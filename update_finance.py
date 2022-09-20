import os
import gspread
import calendar

from txn_types import TxnData, TxnFile


_SPREADSHEET_NAME = 'Spend Tracker v2'
_RANGE = 'A2:E'


def make_sheet(sheet_name) -> gspread.Worksheet:
    """Creates a new sheet from 'Template' sheet in worksheet

    :param sheet_name str: The name of the new sheet to be created
    :retrun: gspread Worksheet obj
    """

    gc = gspread.oauth()
    client = gc.open(_SPREADSHEET_NAME)
    worksheet = client.worksheet("Template")
    worksheet = worksheet.duplicate()
    worksheet.update_title(sheet_name)
    return worksheet


def read_sheet(worksheet: gspread.Worksheet) -> list[TxnData]:
    """Reads txns from a sheet and returns a list of TxnData

    :param worksheet Worksheet: Worksheet object to read from 
    """
    txns = [{"date": txns[0],
             "catagory": txns[1],
             "description": txns[2],
             "price": float(txns[3].replace('£', '').strip()),
             "spender": txns[4]} for txns in worksheet.get(f'{_RANGE}')]
    return txns


def export_to_sheet(txns: list[TxnData], worksheet: gspread.Worksheet) -> None:
    """Takes txns list and exports to google sheets

    :param txns list: list for a month of transactions from csv files
    :param worksheet gspread.Worksheet: gspread Worksheet object to export to
    """

    lst_of_txns = []
    [lst_of_txns.append([value for value in txn.values()]) for txn in txns]
    worksheet.update(f'{_RANGE}{len(lst_of_txns) + 1}', lst_of_txns)
    worksheet.sort((1, 'asc'), range=f'{_RANGE}{len(lst_of_txns) + 1}')


def combine_txns(txns: list[TxnData], txns_from_sheet: list[TxnData]) -> list[TxnData]:
    """Combines txns read from a csv with txns from a worksheet
    
    :param txns list: list of TxnData from csv
    :param txns_from_sheet list: list of TxnData from worksheet
    """
    
    deduped = []
    dupe = set()
    combined = txns + txns_from_sheet
    for txn in combined:
        tupled = tuple(txn.items())
        if tupled not in dupe:
            dupe.add(tupled)
            deduped.append(txn)
    return deduped


if __name__ == "__main__":
    # TODO
    #   If a sheet exists already, don't overwrite the data, append it then sort it
    #       Search for duplicate transactions and don't duplicate data
    #
    #   When a new sheet is added, update the Overview page to include it
    #
    #   Once a csv had been read, don't read it again
    #
    #   Create a Sankey chart from all transactions
    #
    #   Make the year in the sheet title dynamic
    #
    #   Use defaultDicts
    #
    #   Don't dupe uncatagorised txns that have been edited with a catagory

    txns_to_export = {}
    txn_files = [TxnFile.from_name(filename)
                 for filename in os.listdir(f'csv/')]
    for file in txn_files:
        file.extract_txns()
        for month, txns in file.txns.items():
            if month in txns_to_export:
                txns_to_export[month].extend(txns)
            else:
                txns_to_export[month] = txns

    gc = gspread.oauth()
    sheet = gc.open(_SPREADSHEET_NAME)
    for month, txns in txns_to_export.items():
        title = f'{calendar.month_name[month]}_22'
        if title not in [sheet.title for sheet in sheet.worksheets()]:
            worksheet = make_sheet(title)
            export_to_sheet(txns, worksheet)
        else:
            worksheet = sheet.worksheet(title)
            txns_from_sheet = read_sheet(worksheet)
            combined = combine_txns(txns, txns_from_sheet)
            export_to_sheet(combined, worksheet)
