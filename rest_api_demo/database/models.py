# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime

from rest_api_demo.database import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref = db.backref('posts', lazy = 'dynamic'))
    
    def __init__(self, title, body, category, pub_date = None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category
    
    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Category %r>' % self.name


class DateIso(db.TypeDecorator):
    impl = db.DateTime
    
    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.fromisoformat(value)
        return value


class GeoName(db.Model):
    __tablename__ = 'geoname'
    
    geonameid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    asciiname = db.Column(db.String(200), nullable = False)
    alternatenames = db.Column(db.String(10000), nullable = False, index = True)
    latitude = db.Column(db.Float, nullable = False)
    longitude = db.Column(db.Float, nullable = False)
    feature_class = db.Column(db.String(1), nullable = False)
    feature_code = db.Column(db.String(10), nullable = False)
    
    country_code_1 = db.Column(db.String(2), nullable = False)
    country_code_2 = db.Column(db.String(200), nullable = False)
    admin_code_1 = db.Column(db.String(20), nullable = False)
    admin_code_2 = db.Column(db.String(80), nullable = False)
    admin_code_3 = db.Column(db.String(20), nullable = False)
    admin_code_4 = db.Column(db.String(20), nullable = False)
    population = db.Column(db.Integer, nullable = False)
    
    elevation = db.Column(db.Integer, nullable = False)
    dem = db.Column(db.Integer, nullable = False)
    timezone = db.Column(db.String(40), nullable = False)
    modification_date = db.Column(DateIso, nullable = False)
    
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
