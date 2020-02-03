from rest_api_demo.database import db
from rest_api_demo.database.models import GeoName


def seed_database():
    with open('../res/RU.txt') as file:
        for line in file.read().splitlines():
            line_split = line.split('\t')
            geoname = GeoName(*line_split)
            db.session.add(geoname)
        db.session.commit()
