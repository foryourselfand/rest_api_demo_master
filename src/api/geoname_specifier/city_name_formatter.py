from abc import ABC, abstractmethod


class CityNameFormatter(ABC):
    @staticmethod
    @abstractmethod
    def get_city_name_formatted(city_name: str) -> str:
        pass


class CityNameFormatterBasic(CityNameFormatter):
    @staticmethod
    def get_city_name_formatted(city_name: str) -> str:
        return city_name


class CityNameFormatterWithCommas(CityNameFormatter):
    @staticmethod
    def get_city_name_formatted(city_name: str) -> str:
        return f',{city_name},'
