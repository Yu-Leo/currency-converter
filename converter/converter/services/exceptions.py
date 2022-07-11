class GettingDataError(Exception):
    """
    Some error in getting data from API or database
    """

    def __init__(self):
        super().__init__("getting data error")


class ConversionError(Exception):
    """
    Exchange rate of some currency = 0
    """

    def __init__(self):
        super().__init__("exchange rate of some currency = 0")


class DatabaseError(Exception):
    """
    Some error in working with the database
    """

    def __init__(self):
        super().__init__("database error")


class APIError(Exception):
    """
    Some error in getting data from API
    """

    def __init__(self):
        super().__init__("API error")
