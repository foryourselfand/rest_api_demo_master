import flask

from src.database import db
from src.database.models import GeoName
from src.utils.helper import Helper


class Seeder:
    @staticmethod
    def set_up_database(app: flask.app.Flask):
        with app.app_context():
            Seeder.reset_database()
            Seeder.seed_database()
    
    @staticmethod
    def reset_database():
        db.drop_all()
        db.create_all()
    
    @staticmethod
    def seed_database():
        with open(f'{Helper.get_project_root()}/RU.txt') as file:
            for line in file.read().splitlines():
                line_split = line.split('\t')
                
                alternatenames = line_split[3]
                alternatenames_with_commas = f',{alternatenames},'
                line_split[3] = alternatenames_with_commas
                
                geoname = GeoName(*line_split)
                db.session.add(geoname)
            db.session.commit()
