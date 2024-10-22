from flask_restplus import fields

from src.api.restplus import api


class IntegerSafe(fields.Integer):
    def format(self, value):
        try:
            return int(value)
        except ValueError:
            return 0


class StringWithoutCommas(fields.String):
    def format(self, value):
        if value[0] == value[-1] == ',':
            return value[1:-1]
        else:
            return value


class Serializers:
    geoname = api.model('GeoName', {
        'geonameid':         fields.Integer(description='integer id of record in geonames database'),

        'name':              fields.String(description='name of geographical point (utf8) varchar(200)'),
        'asciiname':         fields.String(
                description='name of geographical point in plain ascii characters, varchar(200)'),
        'alternatenames':    StringWithoutCommas(description='alternatenames, comma separated, ascii names'
                                                             'automatically transliterated, convenience attribute '
                                                             'from alternatename table, varchar(10000)'),
        'latitude':          fields.Float(description='latitude in decimal degrees (wgs84)'),
        'longitude':         fields.Float(description='longitude in decimal degrees (wgs84)'),
        'feature class':     fields.String(attribute='feature_class',
                                           description='see http://www.geonames.org/export/codes.html, char(1)'),
        'feature code':      fields.String(attribute='feature_code',
                                           description='see http://www.geonames.org/export/codes.html, varchar(10)'),
        'country code':      fields.String(attribute='country_code_1',
                                           description='ISO-3166 2-letter country code, 2 characters'),
        'cc2':               fields.String(
                attribute='country_code_2',
                description='alternate country codes, comma separated, ISO-3166 2-letter country code, '
                            '200 characters'),
        'admin1 code':       fields.String(
                attribute='admin_code_1',
                description='fipscode (subject to change to iso code), see exceptions below, '
                            'see file admin1Codes.txt '
                            'for display names of this code; varchar(20)'),
        'admin2 code':       fields.String(
                attribute='admin_code_2',
                description='code for the second administrative division, a county in the US, '
                            'see file admin2Codes.txt; '
                            'varchar(80)'),
        'admin3 code':       fields.String(attribute='admin_code_3',
                                           description='code for third level administrative division, varchar(20)'),
        'admin4 code':       fields.String(attribute='admin_code_4',
                                           description='code for fourth level administrative division, varchar(20)'),
        'population':        fields.Integer(description='bigint (8 byte int)'),
        'elevation':         IntegerSafe(description='in meters, integer'),
        'dem':               fields.Integer(
                description="digital elevation model, srtm3 or gtopo30, average elevation "
                            "of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in "
                            "meters, integer. srtm processed by cgiar/ciat."),
        'timezone':          fields.String(description='the iana timezone id (see file timeZone.txt) varchar(40)'),
        'modification date': fields.Date(attribute='modification_date',
                                         description='date of last modification in yyyy-MM-dd format')
        })

    pagination = api.model('A page of results', {
        'page':     fields.Integer(description='Number of this page of results'),
        'pages':    fields.Integer(description='Total number of pages of results'),
        'per_page': fields.Integer(description='Number of items per page of results'),
        'total':    fields.Integer(description='Total number of results'),
        })

    page_of_geonames = api.inherit('Page of geonames', pagination, {
        'items': fields.List(fields.Nested(geoname))
        })

    comparison = api.model('Comparison of two GeoNames', {
        'geoname_first':         fields.Nested(geoname, description='GeoName of the first city'),
        'geoname_second':        fields.Nested(geoname, description='GeoName of the second city'),
        'north_city_name':       fields.String(description='Name of city which located north'),
        'north_city_name_input': fields.String(description='Input name of city which located north (In Russian)'),
        'is_timezone_different': fields.Boolean(),
        'timezone_difference':   fields.Integer(
                description="In hours, Absolute value (whatever city first timezone different from city second "
                            "timezone, "
                            "or opposite - don't matter, so signs is unnecessary)")
        })

    hints = api.model('Hint with possible city name variants', {
        'founded':     fields.Boolean(description='Is exact match was founded'),
        'total':       fields.Integer(description='Total number of suggestions'),
        'suggestions': fields.List(fields.String())
        })
