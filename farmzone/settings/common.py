from __future__ import unicode_literals, absolute_import

import os

import dj_database_url
import dj_email_url
import i18n
from celery.schedules import crontab


def skip_unknown_host_error(record):
    if "Invalid HTTP_HOST header" in record.msg:
        return False
    return True


def is_ec2_linux():
    """Detect if we are running on an EC2 Linux Instance
        See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    try:
        from urllib2 import urlopen
    except:
        from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    response = None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        return response.read()
    except:
        return None
    finally:
        if response:
            response.close()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'k#w5#zqz5@rqugu@z=*4p-96(p2y*m_kn5fnx_cf_mz9(+#7i^')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ElasticBeanstalk healthcheck sends requests with host header = internal ip
# So we detect if we are in elastic beanstalk,
# and add the instances private ip address
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.1.0.230', 'farmzone-dev.ap-south-1.elasticbeanstalk.com', 'www.a3agri.com', 'a3agri.com']
private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'django_fsm',
    'fsm_admin',
    'django_fsm_log',
    'push_notifications',
    'django.contrib.humanize',
    'django_celery_beat',
    'ajax_select',

    # Health Check
    'health_check',                             # required
    'health_check.db',                          # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.celery',              # requires celery
    'mathfilters',
    'farmzone',
    'farmzone.core',
    'farmzone.sellers',
    'farmzone.catalog',
    'farmzone.order',
    'farmzone.buyers',
    'farmzone.support',
    #'trringo.suppliers',
#    'farmzone.send_push_notifications',
    'farmzone.authentication',
#    'farmzone.orders',
#    'farmzone.farmers',
#    'farmzone.pricing',
#    'farmzone.cca',
#    'farmzone.pricing_manager',
#    'farmzone.supply_manager',
#    'farmzone.promotions',
#    'farmzone.marketplace_engine',
#    'farmzone.finance',
#    'farmzone.farmzone_live',
#    'farmzone.hubs',

    # Django Two Factor
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_hotp',
    'django_otp.plugins.otp_static',
    'two_factor'
]

MIDDLEWARE = [
    'bugsnag.django.middleware.BugsnagMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'farmzone.util_config.middleware.RBACMiddleware',
    'django_otp.middleware.OTPMiddleware',
]

ROOT_URLCONF = 'farmzone.util_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'farmzone.util_config.context_processors.from_settings'
            ],
        },
    },
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'farmzone.util_config.rest_customization.CustomPagination',
    'PAGINATE_BY': 10,
    'EXCEPTION_HANDLER': 'farmzone.util_config.custom_exception_response.custom_exception_handler'
}

WSGI_APPLICATION = 'farmzone.util_config.wsgi.application'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'farmzone',
       'USER': 'root',
       'PASSWORD': 'root',
       'HOST': 'localhost',
       'PORT': '3306',
       'TEST': {
            'NAME': 'test_farmzone',
            'USER': 'root',
            'PASSWORD': 'root'
       }
    }
}

# Use the database configuration defined in environment variable DATABASE_URL
db_from_env = dj_database_url.config(conn_max_age=10)
DATABASES['default'].update(db_from_env)

# Get configuration of email from environment variables
EMAIL_URL = os.environ.get('EMAIL_URL')
SENDGRID_USERNAME = os.environ.get('SENDGRID_USERNAME')
SENDGRID_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
if not EMAIL_URL and SENDGRID_USERNAME and SENDGRID_PASSWORD:
    EMAIL_URL = 'smtp://%s:%s@smtp.sendgrid.net:587/?tls=True' % (
        SENDGRID_USERNAME, SENDGRID_PASSWORD)
email_config = dj_email_url.parse(EMAIL_URL or 'console://')

EMAIL_BACKEND = email_config['EMAIL_BACKEND']
EMAIL_FILE_PATH = email_config['EMAIL_FILE_PATH']
EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']
EMAIL_HOST = email_config['EMAIL_HOST']
EMAIL_PORT = email_config['EMAIL_PORT']
EMAIL_USE_TLS = email_config['EMAIL_USE_TLS']
EMAIL_USE_SSL = email_config['EMAIL_USE_SSL']

FCM_SERVER_KEY = os.environ.get('FCM_SERVER_KEY')

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": FCM_SERVER_KEY,
    "FCM_ERROR_TIMEOUT": 1000
}


AUTH_USER_MODEL = 'core.User'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# In elastic beanstalk, LOG_DIR is set to /opt/python/log
# See .ebextensions/farmzone.config
# All other environments, LOG_DIR is empty, which means
# log files are created in current working directory
LOG_DIR = os.environ.get('LOG_DIR', '')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'skip_unknown_host_error': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_unknown_host_error
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'skip_unknown_host_error'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': 10,
            'filters': ['skip_unknown_host_error'],
            'filename': os.path.join(LOG_DIR, 'farmzone.log'),
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true', 'skip_unknown_host_error'],
            'formatter': 'verbose'
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10,
            'filename': os.path.join(LOG_DIR, 'queries.log'),
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
        'bugsnag': {
            'level': 'ERROR',
            'filters': ['skip_unknown_host_error'],
            'class': 'bugsnag.handlers.BugsnagHandler',
        },
        'celery_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'celery-worker.log'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
            'encoding': 'utf-8',
            'filters': ['skip_unknown_host_error'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'farmzone': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console', 'celery_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['sql'],
            'propagate': False,
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'documents')
MEDIA_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL= '/accounts/login/'
OTP_LOGIN_URL = 'two_factor:login'


WHITENOISE_ROOT = os.path.join(PROJECT_ROOT, 'public')
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]


MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

MEDIA_URL = '/media/'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}

#DISTANCE_UNIT = 'metric'

# ORDER_CANCELLATION_REASONS = [
#     "busy_with_another_order",
#     "implement_not_working_condition",
#     "tractor_not_working_condition",
#     "farmer_not_ready_for_operation",
#     "farmer_not_allowing_operation",
#     "farmer_not_available",
#     "incorrect_implement",
#     "driver_not_available",
#     "crop_damaged",
#     "too_far_from_house",
#     "other"
# ]

i18n.load_path.append('farmzone/i18n')
#TRACTOR_TYPES = ["TRACTOR","HARVESTER","BALER"]
PREFERRED_TIMEZONE = os.environ.get('PREFERRED_TIMEZONE', 'Asia/Kolkata')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'farmzone-dev')
AWS_DEFAULT_ACL = 'private'
S3_USE_SIGV4 = True
AWS_REGION='ap-south-1'

AWS_STORAGE_PUBLIC_BUCKET_NAME = os.environ.get('AWS_STORAGE_PUBLIC_BUCKET_NAME', 'farmzone-dev-public')

# from collections import namedtuple
#
# Role = namedtuple("Role", "app required_role url_structure default_page description card_name")
# ROLES = [
#     Role("CCA", "CCA", "^/cca.*", "/cca/orders", "For Call Center Agent", "Agent"),
#     Role("supply_manager", "SupplyManager", "^/supply-manager.*", "/supply-manager/home", "For Supply Manager", "Inventory"),
#     Role("bungee", "BUNGEE", "^/bungee.*", "/bungee/", "For Marketing Manager", "Bungee"),
#     Role("admin", "Admin", "^/admin.*", "/admin/", "For Admin", "Keys"),
#     Role("finance", "Finance", "^/finance.*", "/finance/home", "For Finance", "Finance"),
#     Role("farmzone_live", "OperationsManager", "^/live.*", "/live/home", "For Operations Manager", "farmzone Live"),
# ]
#
# BUNGEE_APP = namedtuple("APP", "app default_page description card_name")
# BUNGEE_APPS = [
#     BUNGEE_APP("Pricing", "/bungee/pricing/home", "For Pricings", "Pricing"),
#     BUNGEE_APP("Promotions", "/bungee/promotions/home", "For Promotions", "Promotions"),
# ]

CAN_SEND_SMS = True
OTP_TOTP_ISSUER = "Farmzone Platform"

########## CELERY
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_BROKER_TRANSPORT = 'redis'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TIMEZONE=PREFERRED_TIMEZONE
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 86400}
# CELERY_BEAT_SCHEDULE = {
#     'daily_performance_task': {
#         'task': 'farmzone.hubs.tasks.update_daily_performance_summary',
#         'schedule': crontab(hour=23, minute=30) # Execute daily at midnight.
#     },
#     'implement_status_check_task': {
#         'task': 'farmzone.suppliers.tasks.cancel_inactive_implement_orders',
#         'schedule': crontab(hour=18, minute=0) # Execute daily at 6PM.
#     }
# }
# In development, all tasks will be executed locally by blocking until the task returns
########## END CELERY

# Table Records' Pagination variables
PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT = 10
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('CACHE_URL', 'redis://127.0.0.1:6379/0'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
