from typing import TypedDict


class TxnData(TypedDict):
    date: str
    catagory: str
    description: str
    price: float
    spender: str
