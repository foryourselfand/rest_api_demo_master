import logging

from flask import request
from flask_restplus import Resource

from rest_api_demo.api.business import Business
from rest_api_demo.api.parsers import Parsers
from rest_api_demo.api.restplus import api
from rest_api_demo.api.serializers import Serializers
from rest_api_demo.database.models import Comparison, GeoName

log = logging.getLogger(__name__)

ns = api.namespace('geonames/task_', description = 'Operations related to GeoNames')


@ns.route('1/by_geonameid/<int:geonameid>')
class GeoNameById(Resource):
    @api.response(404, 'GeoName not found.')
    @api.marshal_with(Serializers.geoname)
    def get(self, geonameid: int):
        """
        Returns a GeoName by geonameid.
        """
        return GeoName.query.filter(GeoName.geonameid == geonameid).one()


@ns.route('2/paginated')
class GeoNamePaginated(Resource):
    @api.expect(Parsers.pagination_arguments)
    @api.marshal_with(Serializers.page_of_geonames)
    def get(self):
        """
        Returns list of GeoNames.
        """
        args = Parsers.pagination_arguments.parse_args(request)
        page: int = args.get('page')
        per_page: int = args.get('per_page')
        
        geoname_query = GeoName.query
        geoname_page = geoname_query.paginate(page, per_page, error_out = False)
        
        return geoname_page


@ns.route('3/compare_two_cities')
class GeoNameCompareTwoCities(Resource):
    @api.expect(Parsers.comparison_arguments)
    @api.response(404, 'GeoName not found.')
    @api.marshal_with(Serializers.comparison)
    def get(self):
        """
        Returns the result of comparing two cities
        """
        args = Parsers.comparison_arguments.parse_args(request)
        
        city_first: str = args.get('city_first')
        city_second: str = args.get('city_second')
        
        geoname_first: GeoName = Business.get_geoname_specified(city_first)
        geoname_second: GeoName = Business.get_geoname_specified(city_second)
        
        north_city_name: str = Business.get_north_city_name(geoname_first, geoname_second)
        north_city_name_input: str = Business.get_north_city_name_input(geoname_first, geoname_second,
                                                                        city_first, city_second)
        timezone_difference: int = Business.get_timezone_difference(geoname_first, geoname_second)
        is_timezone_different: bool = Business.get_is_timezone_different(timezone_difference)
        
        return Comparison(geoname_first, geoname_second,
                          north_city_name, north_city_name_input,
                          is_timezone_different, timezone_difference)
