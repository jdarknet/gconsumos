import os,sys
import socket

reload(sys)
sys.setdefaultencoding("utf-8")

ADMINS = (
    ('info', 'info@infinityloop.es'),
    )

PROJECT_DIR = os.path.dirname(__file__)
BUILDOUT_DIR  = PROJECT_DIR
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

servidor = socket.gethostname()
if servidor=='julian-desktop':
    DEBUG=False
else:
    DEBUG=True

TEMPLATE_DEBUG = DEBUG
EMAIL_HOST='localhost'
EMAIL_PORT =25
MANAGERS = ADMINS


MANAGERS = ADMINS
DATABASE = PROJECT_ROOT+'/datos/datos.ccd'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DATABASE,                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Atlantic/Canary'
TIME_INPUT_FORMATS = ('%I:%M %p', '%I:%M%p', '%H:%M:%S', '%H:%M')
TIME_FORMAT = 'h:i A'
DATE_FORMAT = "%d-%m-%Y"
LANGUAGE_CODE = 'Es-es'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = PROJECT_ROOT+"/static/"
STATIC_URL = '/static/'


FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.MemoryFileUploadHandler",
                        "django.core.files.uploadhandler.TemporaryFileUploadHandler",)


STATICFILES_DIRS = ( PROJECT_ROOT+"/html",)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


SECRET_KEY = '^73!0%y6#u*qm36xg=_j@d&amp;ho-wz#)n)0f(+)xz13sab1d$&amp;7g'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
    )

ROOT_URLCONF = 'gconsumos.urls'

DAJAXICE_MEDIA_PREFIX="dajaxice"


WSGI_APPLICATION = 'gconsumos.wsgi.application'

TEMPLATE_DIRS = (PROJECT_ROOT+'/templates',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'dajaxice',
    'dajax',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'ajax_select',
    'web',
    'maestros',
    'comunicacion',
    'lecturas',
    'django.contrib.admin',


)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        },

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
            },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html' :True,
        },

        'log_file':{
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(PROJECT_ROOT, 'logs/weblogger.log'),
                'maxBytes': '16777216', # 16megabytes
                'formatter': 'simple',
            },

        },

    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
            },
        'lecturas.GetDataFromCurrentCostMeter': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'lecturas.currentcostdb': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': False,
            }
    }
}

AJAX_LOOKUP_CHANNELS = {

    'terceros'  : {'model':'maestros.Terceros', 'search_field':'denominacion'}
}
# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'