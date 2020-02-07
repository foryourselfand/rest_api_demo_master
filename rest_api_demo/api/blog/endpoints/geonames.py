import logging

from flask import abort, request
from flask_restplus import marshal, Resource

from rest_api_demo.api.blog.business import Business
from rest_api_demo.api.blog.parsers import comparison_arguments, pagination_arguments
from rest_api_demo.api.blog.serializers import comparison, geoname, page_of_geonames
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import GeoName

f

log = logging.getLogger(__name__)

ns = api.namespace('geonames', description = 'Operations related to GeoNames')


@ns.route('/by_geonameid/<int:geonameid>')
class GeoNameId(Resource):
    @api.marshal_with(geoname)
    @api.response(404, 'GeoName not found.')
    def get(self, geonameid: int):
        """
        Returns a geoname by geonameid.
        """
        return GeoName.query.filter(GeoName.geonameid == geonameid).one()


@ns.route('/by_page')
class GeoNamePage(Resource):
    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_geonames)
    def get(self):
        """
        Returns list of geonames.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        
        geoname_query = GeoName.query
        geoname_page = geoname_query.paginate(page, per_page, error_out = False)
        
        return geoname_page


@ns.route('/compare_two')
class GeoNameCompare(Resource):
    @api.expect(comparison_arguments)
    @api.response(404, 'GeoName not found.')
    def get(self):
        args = comparison_arguments.parse_args(request)
        
        city_first = args.get('city_first')
        city_second = args.get('city_second')
        
        geoname_first = self.get_geoname(city_first)
        geoname_second = self.get_geoname(city_second)
        
        if not geoname_first or not geoname_second:
            abort(404, 'GeoName not found.')
        
        north_city_name: str = Business.get_north_city_name(geoname_first, geoname_second)
        
        data = {'geoname_first':         geoname_first,
                'geoname_second':        geoname_second,
                'north_city_name':       north_city_name,
                'is_timezone_different': True,
                'timezone_difference':   -1}
        return marshal(data, comparison)
    
    def get_geoname(self, city_name: str) -> GeoName:
        city_name_with_comma = city_name + ','
        geoname_query = GeoName.query.filter(GeoName.alternatenames.contains(city_name_with_comma)). \
            order_by(GeoName.population).first()
        return geoname_query
