from .common import *


########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_ALWAYS_EAGER = True
########## END CELERY

TWO_FACTOR_API_KEY = os.environ.get('TWO_FACTOR_API_KEY', '5e614f64-5bd9-11e7-94da-0200cd936042')
GOOGLE_DISTANCE_MATRIX_API_KEY = os.environ.get('GOOGLE_DISTANCE_MATRIX_API_KEY')
EXOTEL_SID = os.environ.get('EXOTEL_SID')
EXOTEL_TOKEN = os.environ.get('EXOTEL_TOKEN')
EXO_PHONE = os.environ.get('EXO_PHONE')
IVR_AUTH_TOKEN = os.environ.get('IVR_AUTH_TOKEN')

INSTALLED_APPS.insert(0, 'django_nose')
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=farmzone'
]
