CATAGORIES = {
    'Food': ['tesco', 'lidl', 'sainsburry', 'supermarket', 'morrison', 'co-op', 'waitrose', 'CROUCH BUTCHERS'],
    'Transport': ['tfl', 'trainline', 'petrol', 'shell', 'bearsted station', 'RINGGO', 'ARRIVA', 'ROAD SERVICE', 'UBER TRIP', 'APCOA PARKING', 'LSER PREBOOK'],
    'Entertainment': ['steam game', 'weatherspoons', 'Nintendo', 'MUGGLETON INN', 'YE OLDE THIRSTY PIG', 'CHESS COM', 'Jagex', 'Badminton', 'Tiger Moth', 'Greene King', 'Maidstone Leisure', 'Steam Purchase', 'HERBALIST', 'The Source', 'Century Club'],
    'Clothes': ['asos', 'shien', 'oh polly', 'uniqlo', 'Primark'],
    'Personal': ['Lush UK', 'MONKEY HAIR'],
    'Utilities': ['ee limited', 'REFERENCE - Phone'],
    'NE Food': ['just eat', 'deliveroo', 'starbucks', 'marks & spencer', 'MCDONALDS', 'Semoorg', 'INDIA VILLAGE', 'Greggs', 'KFC', 'FATEEMA', 'COSTA', 'DOMINOS PIZZA', 'GAILS BLACKFRIARS', 'NANDO'],
    'Transfers': ['payment received', 'Cado Payroll', 'PAYMENT TO AMERICAN EXPRESS', 'FROM Coinbase', 'TRANSFER TO MR JACOB', 'TRANSFER FROM MR JACOB','PAYMENT TO VANGUARD', 'FROM ICOMERA', 'REFERENCE Credit Card', 'PAID IN AT ATM'],
    'Other': ['CASH WITHDRAWAL', 'CRO TOPUP', 'T K MAXX', 'FOREIGN CURRENCY']
}

def catagorise(description) -> str:
    """Takes txn description and returns spend catagory

    :param str description: Description of txn and vendor
    :return: Spend catagory
    """

    for catagory, vendor_list in CATAGORIES.items():
        for vendor in vendor_list:
            if vendor.lower() in description.lower():
                return catagory
    return 'Unknown'
