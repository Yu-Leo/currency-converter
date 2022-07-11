class GettingDataError(Exception):
    """
    Some error in getting data from API or database
    """
    pass


class ConversionError(Exception):
    """
    Exchange rate of some currency = 0
    """
    pass


class DatabaseError(Exception):
    """
    Some error in working with the database
    """
    pass


class APIError(Exception):
    """
    Some error in getting data from API
    """
    pass
