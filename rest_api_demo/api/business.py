import datetime

import pytz

from rest_api_demo.database.models import GeoName


class Business:
    @staticmethod
    def get_geoname_specified(city_name: str) -> GeoName:
        city_name_with_comma = f',{city_name},'
        geoname_query = GeoName.query \
            .filter(GeoName.feature_class == 'P') \
            .filter(GeoName.alternatenames.contains(city_name_with_comma)). \
            order_by(GeoName.population.desc())
        return geoname_query.first_or_404()
    
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
