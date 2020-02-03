# Flask settings


FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = True

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///geoname.sqlite'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Logging settings
from rest_api_demo.utils import helper
logging_conf_path = f'{helper.get_project_root()}/logging.conf'

# Other
url_prefix = '/internship'
