from abc import ABC, abstractmethod


class IDatabase(ABC):
    """
    Interface for classes working with database
    """

    # Currencies values

    @abstractmethod
    def set_value(self, key: str, value: float) -> None:
        """
        :param key: name of currency
        :param value: the cost of one dollar (USD) in the currency
        """
        pass

    @abstractmethod
    def get_value(self, key: str) -> float:
        """
        :param key: name of currency
        :return: the cost of one dollar (USD) in the currency
        """
        pass

    # Currencies list

    @abstractmethod
    def set_list(self, currencies_list: list[str]) -> None:
        """
        :param currencies_list: list with names of currencies
        """
        pass

    @abstractmethod
    def get_list(self) -> list[str]:
        """
        :return: list with names of currencies
        """
        pass
