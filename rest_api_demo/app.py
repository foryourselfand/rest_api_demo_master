import logging.config

from flask import Blueprint, Flask

from rest_api_demo import settings
from rest_api_demo.api.blog.endpoints.categories import ns as blog_categories_namespace
from rest_api_demo.api.blog.endpoints.geonames import ns as geonames_namespace
from rest_api_demo.api.blog.endpoints.posts import ns as blog_posts_namespace
from rest_api_demo.api.restplus import api
from rest_api_demo.database import db, reset_database
from rest_api_demo.database.seeder import seed_database

logging.config.fileConfig(settings.logging_conf_path)
log = logging.getLogger(__name__)

app = Flask(__name__)


def configure_app():
    # Flask settings
    app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    app.config['FLASK_DEBUG'] = settings.FLASK_DEBUG
    
    # Flask-Restplus settings
    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    
    # SQLAlchemy settings
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS


def initialize_app():
    blueprint = Blueprint('api', __name__, url_prefix = settings.url_prefix)
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    api.add_namespace(geonames_namespace)
    app.register_blueprint(blueprint)
    
    db.init_app(app)


def main():
    configure_app()
    initialize_app()
    
    # with app.app_context():
    #     reset_database()
    #     seed_database()
    
    log.info(f'>>>>> Starting development server at http://{settings.FLASK_SERVER_NAME}{settings.url_prefix}/ <<<<<')
    app.run()


if __name__ == "__main__":
    main()
