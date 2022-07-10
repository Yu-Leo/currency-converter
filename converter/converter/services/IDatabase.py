from abc import ABC, abstractmethod


class IDatabase(ABC):
    """
    Interface for classes working with database
    """

    # Currencies values

    @abstractmethod
    def set_currency_value(self, key: str, value: float) -> None:
        """
        :param key: name of currency
        :param value: the cost of one dollar (USD) in the currency
        """
        pass

    @abstractmethod
    def set_currencies_values(self, values: dict[str, float]) -> None:
        """
        :param values: dict with pairs:
        name of currency - the cost of one dollar (USD) in the currency
        """
        pass

    @abstractmethod
    def get_currency_value(self, key: str) -> float:
        """
        :param key: name of currency
        :return: the cost of one dollar (USD) in the currency
        """
        pass

    # Currencies list

    @abstractmethod
    def set_currencies_list(self, currencies_list: list[str]) -> None:
        """
        :param currencies_list: list with names of currencies
        """
        pass

    @abstractmethod
    def is_currencies_list_exists(self) -> bool:
        pass

    @abstractmethod
    def get_currencies_list(self) -> list[str]:
        """
        :return: list with names of currencies
        """
        pass
