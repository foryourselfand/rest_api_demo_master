import logging
from typing import Set

from flask import request
from flask_restplus import Resource

from src.api.business import Business
from src.api.parsers import Parsers
from src.api.restplus import api
from src.api.serializers import Serializers
from src.database.models import Comparison, GeoName, Hints

log = logging.getLogger(__name__)

ns = api.namespace('geonames/task_', description='Operations related to GeoNames')


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
        Returns paginated list of GeoNames.
        """
        args = Parsers.pagination_arguments.parse_args(request)
        page: int = args.get('page')
        per_page: int = args.get('per_page')

        geoname_query = GeoName.query
        geoname_page = geoname_query.paginate(page, per_page, error_out=False)

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

        geoname_first: GeoName = Business.get_geonames_matched_full(city_first).first_or_404()
        geoname_second: GeoName = Business.get_geonames_matched_full(city_second).first_or_404()

        north_city_name: str = Business.get_north_city_name(geoname_first, geoname_second)
        north_city_name_input: str = Business.get_north_city_name_input(geoname_first, geoname_second,
                                                                        city_first, city_second)

        timezone_difference: int = Business.get_timezone_difference(geoname_first, geoname_second)
        is_timezone_different: bool = Business.get_is_timezone_different(timezone_difference)

        return Comparison(geoname_first, geoname_second,
                          north_city_name, north_city_name_input,
                          is_timezone_different, timezone_difference)


@ns.route('42/hints/<string:city_name>')
class GeoNameHints(Resource):
    @api.marshal_with(Serializers.hints)
    def get(self, city_name: str):
        """
        Returns hint with possible city name variants
        """
        geonames_matched_full = Business.get_geonames_matched_full(city_name)

        founded: bool = geonames_matched_full.count() != 0

        geonames_matched_part = Business.get_geonames_matched_part(city_name)

        suggestions: Set[str] = Business.get_suggestions(geonames_matched_part, city_name)
        geonames_matched_part_total: int = len(suggestions)

        return Hints(founded, geonames_matched_part_total, suggestions)
