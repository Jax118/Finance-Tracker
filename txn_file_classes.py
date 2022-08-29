import re
import csv
import datetime

from catagories import catagorise


class TxnFile:
    """Base transaction file class, holds transaction data exported from bank or credit card.
    """
    def __init__(self, filename: str):
        """
        :param filename str: csv filename found in /csv/<month>
        """
        self.filename: str = filename
        self.txns: dict = {}


    def extract_txns(self) -> None:
        pass


class Amex(TxnFile):
    """American Express csv data.
    """

    def extract_txns(self) -> None:
        """Takes a given amex csv filename and updates self.txns
        """
        temp_row = {}
        with open(f'csv/{self.filename}', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for count, row in enumerate(csv_reader):
                if count > 0: # Don't use header row
                    month = datetime.datetime.strptime(row[0], "%d/%m/%Y")
                    temp_row['Date'] = row[0]
                    temp_row['Description'] = row[1]
                    temp_row['Spender'] = 'Jake'
                    temp_row['Catagory'] = catagorise(temp_row['Description'])
                    if 'jess' in self.filename:
                        temp_row['Price'] = float(row[4])
                        if 'MISS' in row[2]:
                            temp_row['Spender'] = 'Jess'
                    else:
                        temp_row['Price'] = float(row[2])
                    if month in self.txns:
                        self.txns[month].append(temp_row)
                    else:
                        self.txns[month] = [temp_row]


class Santander(TxnFile):
    """Santander csv data.
    """

    def extract_txns(self) -> None:
        """Takes a given Santander csv filename and updates self.txns
        """
        with open(f'csv/{self.filename}', 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            for count, row in enumerate(csv_reader):
                temp_row = {}
                if count > 4: # Don't use header rows
                    month = datetime.datetime.strptime(row[1], "%d/%m/%Y").month
                    temp_row['Date'] = row[1]
                    temp_row['Catagory'] =  catagorise(row[3])
                    temp_row['Description'] = re.sub(r'\sON\s(\d{2}-){2}\d{4}', '', row[3]).replace('CARD PAYMENT TO ', '').replace('FASTER PAYMENTS RECEIPT ', '')
                    temp_row['Price'] = row[5] if row[5] else row[6]
                    chars = ['£', ',', '\'']
                    for c in chars:
                        temp_row['Price'] = temp_row['Price'].replace(c, '')
                    temp_row['Price'] = float(temp_row['Price']) * - 1 if row[5] else float(temp_row['Price'])
                    temp_row['Spender'] = 'Jake'
                    if 'jess' in self.filename:
                        temp_row['Spender'] = 'Jess'
                    if month in self.txns:
                        self.txns[month].append(temp_row)
                    else:
                        self.txns[month] = [temp_row]
