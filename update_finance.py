import os
import gspread
import calendar

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


def export_to_sheet(txns: dict, sheet: gspread.Worksheet) -> None:
    """Takes txns list and exports to google sheets
    
    :param txns dict: dict for a month of transactions from csv files
    :param sheet gspread.Worksheet: gspread Worksheet object to export to
    """
    sheet.update(f'A2:E{len(txns) + 1}', [[value for value in txn.values()] for txn in txns])
    sheet.sort((1, 'asc'), range=f'A2:E{len(txns) + 1}')


if __name__ == "__main__":
    # TODO
    #   When exporting to sheet, export to corresponding month tab
    #       Take month from filename and create dict = {<month>: <txns_list>}
    #       Insert txns into corresponding tabs and sort
    
    #   Once a csv has had its txns exported, add to exported list and do not export again
    #       Create txt of exported csv files
    #       Append exported csv's to txt and check before opening

    
    txn_files = []
    for filename in os.listdir(f'csv/'):
        if 'amex' in filename:
            txn_files.append(Amex(filename))
        if 'santander' in filename:
            txn_files.append(Santander(filename))

    txns_to_export = {}
    for file in txn_files:
        file.extract_txns()
        for month, txns in file.txns.items():
            if month in txns_to_export:
                txns_to_export[month].append(txns)
            else:
                txns_to_export[month] = txns

    gc = gspread.oauth()
    spreadsheet = gc.open(_SPREADSHEET_NAME)
    for month, txns in txns_to_export.items():
        title = f'{calendar.month_name[month]}_22' # TODO Make year dynamic
        if title not in [sheet.title for sheet in spreadsheet.worksheets()]:
            sheet = make_sheet(title) 
        else:
            sheet = spreadsheet.worksheet(title)
        export_to_sheet(txns, sheet)
