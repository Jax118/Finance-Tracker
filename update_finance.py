import os
import gspread
import calendar

from txn_data_type import TxnData
from txn_file_classes import Amex, Santander


_SPREADSHEET_NAME = 'Spend Tracker v2'

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


def read_sheet(sheet_name) -> dict:
    """Reads txns from a sheet and returns a dict
    
    :param sheet_name str: Sheet name to read from 
    """
    
    raise NotImplementedError

def export_to_sheet(txns: list[TxnData], worksheet: gspread.Worksheet) -> None:
    """Takes txns list and exports to google sheets
    
    :param txns list: list for a month of transactions from csv files
    :param worksheet gspread.Worksheet: gspread Worksheet object to export to
    """
    
    lst_of_txns = []
    [lst_of_txns.append([value for value in txn.values()]) for txn in txns]
    worksheet.update(f'A2:E{len(lst_of_txns) + 1}', lst_of_txns)
    worksheet.sort((1, 'asc'), range=f'A2:E{len(lst_of_txns) + 1}')


if __name__ == "__main__":
    # TODO
    #   If a sheet exists already, don't overwrite the data, append it then sort it
    #       Search for duplicate transactions and don't duplicate data
    #
    #   When a new sheet is added, update the Overview page to include it
    #
    #   Create a Sankey chart from all transactions
    #
    #   Make the year in the sheet title dynamic


    txn_files = []
    for filename in os.listdir(f'csv/'):
        if '.csv' in filename:
            if 'amex' in filename: # TODO Could be better with classmethods?
                txn_files.append(Amex(filename))
            if 'santander' in filename:
                txn_files.append(Santander(filename))

    txns_to_export = {}
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
        worksheet = make_sheet(title) if title not in [sheet.title for sheet in sheet.worksheets()] else sheet.worksheet(title)
        export_to_sheet(txns, worksheet)
