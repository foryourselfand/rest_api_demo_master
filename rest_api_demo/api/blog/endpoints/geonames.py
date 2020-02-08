import logging

from flask import request
from flask_restplus import Resource

from rest_api_demo.api.blog.business import Business
from rest_api_demo.api.blog.parsers import comparison_arguments, pagination_arguments
from rest_api_demo.api.blog.serializers import comparison, geoname, page_of_geonames
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import Comparison, GeoName

log = logging.getLogger(__name__)

ns = api.namespace('geonames/task_', description = 'Operations related to GeoNames')


@ns.route('1/by_geonameid/<int:geonameid>')
class GeoNameById(Resource):
    @api.response(404, 'GeoName not found.')
    @api.marshal_with(geoname)
    def get(self, geonameid: int):
        """
        Returns a geoname by geonameid.
        """
        return GeoName.query.filter(GeoName.geonameid == geonameid).one()


@ns.route('2/paginated')
class GeoNamePaginated(Resource):
    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_geonames)
    def get(self):
        """
        Returns list of geonames.
        """
        args = pagination_arguments.parse_args(request)
        page: int = args.get('page', 1)
        per_page: int = args.get('per_page', 10)
        
        geoname_query = GeoName.query
        geoname_page = geoname_query.paginate(page, per_page, error_out = False)
        
        return geoname_page


@ns.route('3/compare_two_cities')
class GeoNameCompareTwoCities(Resource):
    @api.expect(comparison_arguments)
    @api.response(404, 'GeoName not found.')
    @api.marshal_with(comparison)
    def get(self):
        """
        Temp description
        """
        args = comparison_arguments.parse_args(request)
        
        city_first: str = args.get('city_first')
        city_second: str = args.get('city_second')
        
        geoname_first: GeoName = self.get_geoname(city_first)
        geoname_second: GeoName = self.get_geoname(city_second)
        
        north_city_name: str = Business.get_north_city_name(geoname_first, geoname_second)
        timezone_difference: int = Business.get_timezone_difference(geoname_first, geoname_second)
        is_timezone_different: bool = Business.get_is_timezone_different(timezone_difference)
        
        return Comparison(geoname_first, geoname_second, north_city_name, is_timezone_different, timezone_difference)
    
    def get_geoname(self, city_name: str) -> GeoName:
        city_name_with_comma = f',{city_name},'
        geoname_query = GeoName.query \
            .filter(GeoName.feature_class == 'P') \
            .filter(GeoName.alternatenames.contains(city_name_with_comma)). \
            order_by(GeoName.population.desc())
        return geoname_query.first_or_404()
