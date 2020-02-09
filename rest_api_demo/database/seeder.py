import flask

from rest_api_demo.database import db
from rest_api_demo.database.models import GeoName


class Seeder:
    @staticmethod
    def set_up(app: flask.app.Flask):
        with app.app_context():
            Seeder.reset_database()
            Seeder.seed_database()
    
    @staticmethod
    def reset_database():
        db.drop_all()
        db.create_all()
    
    @staticmethod
    def seed_database():
        with open('../res/RU.txt') as file:
            for line in file.read().splitlines():
                line_split = line.split('\t')
                
                alternatenames = line_split[3]
                alternatenames_with_commas = f',{alternatenames},'
                line_split[3] = alternatenames_with_commas
                
                geoname = GeoName(*line_split)
                db.session.add(geoname)
            db.session.commit()
