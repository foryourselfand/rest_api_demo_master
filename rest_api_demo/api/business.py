import datetime
from typing import Set

import pytz
from flask_sqlalchemy import BaseQuery

from rest_api_demo.api.geoname_specifier.city_name_formatter import (CityNameFormatter, CityNameFormatterBasic,
                                                                     CityNameFormatterWithCommas, )
from rest_api_demo.api.geoname_specifier.geoname_sorter import (GeoNameSorter, GeoNameSorterBasic,
                                                                GeoNameSorterPopulationDescending, )
from rest_api_demo.database.models import GeoName


class Business:
    @staticmethod
    def get_geonames_specified(city_name: str,
                               city_name_formatter: CityNameFormatter = CityNameFormatterBasic(),
                               geoname_sorter: GeoNameSorter = GeoNameSorterBasic()) -> BaseQuery:
        
        city_name_formatter: str = city_name_formatter.get_city_name_formatted(city_name)
        
        geoname_query: BaseQuery = GeoName.query \
            .filter(GeoName.feature_class == 'P') \
            .filter(GeoName.alternatenames.contains(city_name_formatter))
        geoname_query_sorted: BaseQuery = geoname_sorter.get_geonames_sorted(geoname_query)
        
        return geoname_query_sorted
    
    @staticmethod
    def get_geonames_matched_full(city_name: str) -> BaseQuery:
        return Business.get_geonames_specified(city_name,
                                               CityNameFormatterWithCommas(), GeoNameSorterPopulationDescending())
    
    @staticmethod
    def get_geonames_matched_part(city_name: str) -> BaseQuery:
        return Business.get_geonames_specified(city_name)
    
    @staticmethod
    def get_north_city_name(geoname_first: GeoName, geoname_second: GeoName) -> str:
        if geoname_first.latitude > geoname_second.latitude:
            return geoname_first.name
        else:
            return geoname_second.name
    
    @staticmethod
    def get_north_city_name_input(geoname_first: GeoName, geoname_second: GeoName,
                                  input_name_first: str, input_name_second: str) -> str:
        if geoname_first.latitude > geoname_second.latitude:
            return input_name_first
        else:
            return input_name_second
    
    @staticmethod
    def get_timezone_difference(geoname_first: GeoName, geoname_second: GeoName) -> int:
        timezone_first = pytz.timezone(geoname_first.timezone)
        timezone_second = pytz.timezone(geoname_second.timezone)
        
        now = datetime.datetime.now()
        localize_first = timezone_first.localize(now)
        localize_second = timezone_second.localize(now)
        
        time_difference = abs(int((localize_second - localize_first).total_seconds() / 3600))
        
        return time_difference
    
    @staticmethod
    def get_is_timezone_different(timezone_difference: int) -> bool:
        return timezone_difference != 0
    
    @staticmethod
    def get_suggestions(geonames: BaseQuery, city_name: str) -> Set[str]:
        suggestions: Set[str] = set()
        
        for geoname in geonames:
            alternatenames: str = geoname.alternatenames
            alternatenames_without_commas = alternatenames[1:-1]
            alternatenames_split = alternatenames_without_commas.split(',')
            
            for alternatename in alternatenames_split:
                if city_name in alternatename:
                    suggestions.add(alternatename)
        
        return suggestions
