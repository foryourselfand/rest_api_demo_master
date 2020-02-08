import datetime

import pytz

from rest_api_demo.database import db
from rest_api_demo.database.models import Category, GeoName, Post


class Business:
    @staticmethod
    def get_north_city_name(geoname_first: GeoName, geoname_second: GeoName) -> str:
        if geoname_first.latitude > geoname_second.latitude:
            return geoname_first.name
        else:
            return geoname_second.name
    
    @staticmethod
    def get_timezone_difference(geoname_first: GeoName, geoname_second: GeoName) -> int:
        timezone_first = pytz.timezone(geoname_first.timezone)
        timezone_second = pytz.timezone(geoname_second.timezone)
        
        now = datetime.datetime.now()
        localize_first = timezone_first.localize(now)
        localize_second = timezone_second.localize(now)
        
        time_difference = abs(int((localize_second - localize_first).total_seconds() / 3600))
        
        return time_difference
    
    @staticmethod
    def get_is_timezone_different(timezone_difference: int) -> bool:
        return timezone_difference != 0


def create_blog_post(data):
    title = data.get('title')
    body = data.get('body')
    category_id = data.get('category_id')
    category = Category.query.filter(Category.id == category_id).one()
    post = Post(title, body, category)
    db.session.add(post)
    db.session.commit()


def update_post(post_id, data):
    post = Post.query.filter(Post.id == post_id).one()
    post.title = data.get('title')
    post.body = data.get('body')
    category_id = data.get('category_id')
    post.category = Category.query.filter(Category.id == category_id).one()
    db.session.add(post)
    db.session.commit()


def delete_post(post_id):
    post = Post.query.filter(Post.id == post_id).one()
    db.session.delete(post)
    db.session.commit()


def create_category(data):
    name = data.get('name')
    category_id = data.get('id')
    
    category = Category(name)
    if category_id:
        category.id = category_id
    
    db.session.add(category)
    db.session.commit()


def update_category(category_id, data):
    category = Category.query.filter(Category.id == category_id).one()
    category.name = data.get('name')
    db.session.add(category)
    db.session.commit()


def delete_category(category_id):
    category = Category.query.filter(Category.id == category_id).one()
    db.session.delete(category)
    db.session.commit()
