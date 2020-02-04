import logging

from flask import request
from flask_restplus import Resource

from rest_api_demo.api.blog.parsers import pagination_arguments
from rest_api_demo.api.blog.serializers import geoname, page_of_geonames
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import GeoName

log = logging.getLogger(__name__)

ns = api.namespace('geonames', description = 'Operations related to GeoNames')


@api.response(404, 'GeoName not found.')
@ns.route('/by_geonameid/<int:geonameid>')
class GeoNameId(Resource):
    
    @api.marshal_with(geoname)
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
