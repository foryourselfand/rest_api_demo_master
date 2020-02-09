from src.utils.helper import Helper

# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = True

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = f'sqlite:///{Helper.get_project_root()}/res/geoname.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Logging settings
logging_conf_path = f'{Helper.get_project_root()}/res/logging.conf'

# Other
url_prefix = '/internship'
