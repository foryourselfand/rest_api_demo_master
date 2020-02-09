from abc import ABC, abstractmethod

from flask_sqlalchemy import BaseQuery

from src.database.models import GeoName


class GeoNameSorter(ABC):
    @staticmethod
    @abstractmethod
    def get_geonames_sorted(geonames: BaseQuery) -> BaseQuery:
        pass


class GeoNameSorterBasic(GeoNameSorter):
    @staticmethod
    def get_geonames_sorted(geonames: BaseQuery) -> BaseQuery:
        return geonames


class GeoNameSorterPopulationDescending(GeoNameSorter):
    @staticmethod
    def get_geonames_sorted(geonames: BaseQuery) -> BaseQuery:
        return geonames.order_by(GeoName.population.desc())
