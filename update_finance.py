import os

import gspread

from txn_file_classes import Amex, Santander

def make_sheet(sheet_name) -> gspread.Worksheet:
    """Creates a new sheet from 'Template' sheet in worksheet

    :param sheet_name str: The name of the new sheet to be created
    :retrun: gspread Worksheet obj
    """
    gc = gspread.oauth()
    client = gc.open("Spend Tracker v2")
    worksheet = client.worksheet("Template")
    worksheet = worksheet.duplicate()
    worksheet.update_title(sheet_name)
    return worksheet


def export_to_sheet(txns, sheet) -> None:
    """Takes txns list and exports to google sheets
    
    :param txns list: list of transactions from csv files
    :param sheet gspread.Worksheet: gspread Worksheet object to export to
    """
    worksheet.update(f'A2:E{len(txns) + 1}', txns)
    worksheet.sort((1, 'asc'), range=f'A2:E{len(txns) + 1}')


if __name__ == "__main__":
    month = input("Enter the month: ").lower()

    txn_files = []
    for filename in os.listdir(f'csv/{month}'):
        if month in filename:
            if 'amex' in filename:
                txn_files.append(Amex(filename))
            if 'santander' in filename:
                txn_files.append(Santander(filename))
    txns = []
    for file in txn_files:
        txns.extend(file.extract_txns())
    if txns:
        worksheet = make_sheet(f'{month.upper()}_22')


