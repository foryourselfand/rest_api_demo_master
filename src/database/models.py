from datetime import datetime
from typing import List, Set

from sqlalchemy import Column, Float, Integer, String

from src.database import db


class DateIso(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.fromisoformat(value)
        return value


class GeoName(db.Model):
    __tablename__ = 'geoname'

    geonameid = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    asciiname = Column(String(200), nullable=False)
    alternatenames = Column(String(10000), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    feature_class = Column(String(1), nullable=False)
    feature_code = Column(String(10), nullable=False)

    country_code_1 = Column(String(2), nullable=False)
    country_code_2 = Column(String(200), nullable=False)
    admin_code_1 = Column(String(20), nullable=False)
    admin_code_2 = Column(String(80), nullable=False)
    admin_code_3 = Column(String(20), nullable=False)
    admin_code_4 = Column(String(20), nullable=False)
    population = Column(Integer, nullable=False)

    elevation = Column(Integer, nullable=False)
    dem = Column(Integer, nullable=False)
    timezone = Column(String(40), nullable=False)
    modification_date = Column(DateIso, nullable=False)

    def __init__(self, geonameid, name, asciiname, alternatenames, latitude, longitude, feature_class, feature_code,
                 country_code_1, country_code_2, admin_code_1, admin_code_2, admin_code_3, admin_code_4, population,
                 elevation, dem, timezone, modification_date):
        self.geonameid = geonameid
        self.name = name
        self.asciiname = asciiname
        self.alternatenames = alternatenames
        self.latitude = latitude
        self.longitude = longitude
        self.feature_class = feature_class
        self.feature_code = feature_code
        self.country_code_1 = country_code_1
        self.country_code_2 = country_code_2
        self.admin_code_1 = admin_code_1
        self.admin_code_2 = admin_code_2
        self.admin_code_3 = admin_code_3
        self.admin_code_4 = admin_code_4
        self.population = population
        self.elevation = elevation
        self.dem = dem
        self.timezone = timezone
        self.modification_date = modification_date


class Comparison:
    def __init__(self, geoname_first: GeoName, geoname_second: GeoName,
                 north_city_name: str, north_city_name_input: str,
                 is_timezone_different: bool, timezone_difference: int):
        self.geoname_first = geoname_first
        self.geoname_second = geoname_second
        self.north_city_name = north_city_name
        self.north_city_name_input = north_city_name_input
        self.is_timezone_different = is_timezone_different
        self.timezone_difference = timezone_difference


class Hints:
    def __init__(self, founded: bool, total: int, suggestions: Set[str]):
        self.founded: bool = founded
        self.total: int = total
        self.suggestions: List[str] = list(suggestions)
