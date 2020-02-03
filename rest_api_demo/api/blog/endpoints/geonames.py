import logging

from flask_restplus import Resource

from rest_api_demo.api.blog.serializers import geoname
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import GeoName

log = logging.getLogger(__name__)

ns = api.namespace('geonames', description = 'Operations related to GeoNames')


@api.response(404, 'GeoName not found.')
@ns.route('/<int:geonameid>')
class GeoNameId(Resource):

    @api.marshal_with(geoname)
    def get(self, geonameid: int):
        """
        Returns a geoname by geonameid.
        """
        return GeoName.query.filter(GeoName.geonameid == geonameid).one()
