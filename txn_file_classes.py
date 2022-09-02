import re
import csv
import datetime
from abc import ABC, abstractmethod

from catagories import catagorise
from txn_data_type import TxnData


class TxnFile(ABC):
    """Base transaction file class, holds transaction data exported from bank or credit card.
    """

    def __init__(self, filename: str):
        """
        :param filename str: csv filename found in /csv/<month>

        Attributes:
            filename: The files's name
            txns: A dict with keys of month integer, and values of lists of TxnData
        """

        self.filename: str = filename
        self.txns: dict[int, list[TxnData]] = {}

    @abstractmethod
    def extract_txns(self) -> None:
        pass


class Amex(TxnFile):
    """American Express csv data.
    """

    def extract_txns(self) -> None:
        """Takes a given amex csv filename and updates self.txns
        """

        with open(f'csv/{self.filename}', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for count, row in enumerate(csv_reader):
                txn_data: TxnData = {}
                if count > 0:  # Don't use header row
                    txn_data['date'] = row[0]
                    txn_data['catagory'] = catagorise(row[1])
                    txn_data['description'] = row[1]
                    if 'jess' in self.filename:
                        txn_data['price'] = float(row[4])
                        if 'MISS' in row[2]: txn_data['spender'] = 'Jess'
                    else:
                        txn_data['price'] = float(row[2])
                    txn_data['spender'] = 'Jake'
                    month = datetime.datetime.strptime(
                        txn_data['date'], "%d/%m/%Y").month
                    if month in self.txns:
                        self.txns[month].append(txn_data)
                    else:
                        self.txns[month] = [txn_data]


class Santander(TxnFile):
    """Santander csv data.
    """

    def extract_txns(self) -> None:
        """Takes a given Santander csv filename and updates self.txns
        """

        with open(f'csv/{self.filename}', 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            for count, row in enumerate(csv_reader):
                if count > 4:  # Don't use header rows
                    txn_data: TxnData = {}
                    txn_data['date'] = row[1]
                    txn_data['catagory'] = catagorise(row[3])
                    txn_data['description'] = re.sub(r'\sON\s(\d{2}-){2}\d{4}', '', row[3]).replace('CARD PAYMENT TO ', '').replace('FASTER PAYMENTS RECEIPT ', '')
                    # Invert 'Money in' to be negative to deduct from total spending
                    txn_data['price'] = float(row[5].strip(
                        "£,'") * -1) if row[5] else float(row[6].strip("£,'"))
                    txn_data['spender'] = 'Jake'
                    if 'jess' in self.filename:
                        txn_data['spender'] = 'Jess'
                    month = datetime.datetime.strptime(
                        txn_data['date'], "%d/%m/%Y").month
                    if month in self.txns:
                        self.txns[month].append(txn_data)
                    else:
                        self.txns[month] = [txn_data]
