from .common import *

DEBUG = True
ALLOWED_HOSTS = [
                 'localhost', '127.0.0.1',
                 'farmzone-stage.madu4xnwhw.ap-south-1.elasticbeanstalk.com',
                 'farmzone-prod.madu4xnwhw.ap-south-1.elasticbeanstalk.com',
                 'farmzone-qa.ap-south-1.elasticbeanstalk.com'
               ]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CAN_SEND_SMS = True

SECURE_HSTS_SECONDS=3600
SECURE_HSTS_INCLUDE_SUBDOMAINS=False

# Configure logentries only if LOGENTRIES_KEY is defined in settings
if os.environ.get("LOGENTRIES_KEY", ''):
    LOGGING['handlers']['logentries'] = {
                'level': 'DEBUG',
                'token': os.environ.get("LOGENTRIES_KEY", ''),
                'class': 'logentries.LogentriesHandler',
                'formatter': 'verbose'
            }

    LOGGING['loggers']['farmzone']['handlers'] = ['console', 'file', 'logentries']
    LOGGING['loggers']['celery']['handlers'] = ['console', 'celery_handler', 'logentries']


########## CELERY
# In production, all tasks will be executed in the worker
CELERY_ALWAYS_EAGER = False
########## END CELERY

TWO_FACTOR_API_KEY = os.environ.get('TWO_FACTOR_API_KEY')
GOOGLE_DISTANCE_MATRIX_API_KEY = os.environ.get('GOOGLE_DISTANCE_MATRIX_API_KEY')
EXOTEL_SID = os.environ.get('EXOTEL_SID')
EXOTEL_TOKEN = os.environ.get('EXOTEL_TOKEN')
EXO_PHONE = os.environ.get('EXO_PHONE')
IVR_AUTH_TOKEN = os.environ.get('IVR_AUTH_TOKEN')

BUGSNAG = {
  'api_key': os.environ.get('BUGSNAG_KEY'),
  'project_root': PROJECT_ROOT,
}


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
INSTALLED_APPS.insert(0, 'storages')
