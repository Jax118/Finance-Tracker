CATAGORIES = {
    'Food': ['tesco', 'lidl', 'sainsburry', 'supermarket', 'morrisons', 'co-op', 'waitrose'],
    'Transport': ['tfl', 'trainline', 'petrol', 'shell', 'bearsted station'],
    'Entertainment': ['steam game', 'weatherspoons'],
    'Clothes': ['asos', 'shien', 'oh polly', 'uniqlo'],
    'Personal': [],
    'Utilities': ['ee limited'],
    'NE Food': ['just eat', 'deliveroo', 'starbucks', 'marks & spencer'],
    'Transfers': ['payment received']
}

def catagorise(description) -> str:
    """Takes txn description and returns spend catagory

    :param str description: Description of txn and vendor
    :return: Spend catagory
    """

    for catagory, vendor_list in CATAGORIES.items():
        for vendor in vendor_list:
            if vendor in description.lower():
                return catagory
    return 'Unknown'
