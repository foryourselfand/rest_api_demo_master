import logging
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

from src import settings

log = logging.getLogger(__name__)

api = Api(version = '1.0',
          title = 'Infotecs Internship',
          description = 'Solution of the test task on Python')


@api.errorhandler
def default_error_handler(e):
    log.exception(traceback.format_exc())
    
    if not settings.FLASK_DEBUG:
        return {'message': 'An unhandled exception occurred.'}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
