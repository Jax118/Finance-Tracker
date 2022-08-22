import re
import csv

from catagories import catagorise


class TxnFile:
    """Base transaction file class, holds transaction data exported from bank or credit card.
    """
    def __init__(self, filename: str):
        """
        :param filename str: csv filename found in /csv/<month>
        """
        self.filename: str = filename
        self.txns: list = []


    def extract_txns(self) -> None:
        pass


class Amex(TxnFile):
    """American Express csv data.
    """

    def extract_txns(self) -> None:
        """Takes a given amex csv filename and updates self.txns
        """
        temp_row = {}
        self.txns = []
        with open(f'csv/{self.filename}', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for count, row in enumerate(csv_reader):
                if count > 0: # Don't use header row
                    temp_row['Date'] = row[0]
                    temp_row['Description'] = row[1]
                    temp_row['Spender']('Jake')
                    if 'jess' in self.filename:
                        temp_row['Price'] = float(row[4])
                        if 'MISS' in row[2]:
                            temp_row['Spender']('Jess')
                    else:
                        temp_row['Price'] = float(row[2])
                    temp_row['Catagory'] = catagorise(temp_row['Description'])
                    self.txns.append(temp_row)


class Santander(TxnFile):
    """Santander csv data.
    """

    def extract_txns(self) -> None:
        """Takes a given Santander csv filename and updates self.txns
        """
        temp_row = {}
        self.txns = []
        with open(f'csv/{self.filename}', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for count, row in enumerate(csv_reader):
                if count > 4: # Don't use header rows
                    temp_row['Date'] = row[1]
                    temp_row['Description'] = re.sub(r'\sON\s(\d{2}-){2}\d{4}', '', row[3]).replace('CARD PAYMENT TO ', '')
                    temp_row['Price'] = float(row[5].replace('£', '').replace(',', '')) * -1 if row[5] else float(row[6].replace('£', '').replace(',', '')) # Invert 'Money In' to be negative
                    temp_row['Catagory'] =  catagorise(row[3])
                    temp_row['Spender'] = 'Jake'
                    if 'jess' in self.filename:
                        temp_row['Spender'] = 'Jess'
                    self.txns.append(temp_row)
