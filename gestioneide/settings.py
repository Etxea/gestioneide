import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

#FOR DEV
DEBUG = True

TIME= 1800*60
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE= True
SESSION_COOKIE_AGE = TIME
SESSION_IDLE_TIMEOUT = TIME

#FOR DEV
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev.db",
    }
}

ALLOWED_HOSTS = ["gestion.eide.es","127.0.0.1","localhost"]

PHONENUMBER_DEFAULT_REGION="ES"

TIME_ZONE = "Europe/Madrid"

LANGUAGE_CODE = "es-es"

SITE_ID = int(os.environ.get("SITE_ID", 1))

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static", "dist"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

SECRET_KEY = "%(((6#nr1e+-mzzs&7v3%rdxp(x3$yyp7b)ep^_htq+*iubib3"

SESSION_COOKIE_AGE = 180 * 60 #


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PACKAGE_ROOT, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "account.context_processors.account",
                "pinax_theme_bootstrap.context_processors.theme",
                "gestioneide.context_processors.current_year_processor",
            ],
        },
    },
]

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "gestioneide.middleware.SessionIdleTimeout",
    "gestioneide.middleware.MessagesMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gestioneide.urls"

WSGI_APPLICATION = "gestioneide.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",

    # theme
    "bootstrapform",
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",
    "bootstrap3_datetime",

    # external
    "account",
    "metron",
    "pinax.eventlog",
    'fixture_magic',
    'wkhtmltopdf',
    'pinax.documents',
    "pinax.templates",
    'pinax.messages',
    'phonenumber_field',
    'pinax.notifications',
    'anymail',

    # project
    "gestioneide",
    "alumnos",
    "grupos",
    "profesores",
    "aulas",
    "clases",
    "cursos",
    "calendario",
    "facturacion",
    "evaluacion",
    "informes",
    "libros",
    "imprimir",
    "year",
    "asistencias",
    "turismo",
    "perfil",
    "empresas",
    "centros",
    "mensajes",
    "confirmaciones",
    "sermepa",
    "pasarela",
    "pagosonline",
    "cambridge",
    "matriculas",
    
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug.log',
            'formatter': 'simple',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug.log',
            'formatter': 'simple',
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "xhtml2pdf": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "gestioneide.error": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
        "gestioneide.debug": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST="localhost"
EMAIL_PORT="587"
DEFAULT_FROM_EMAIL = "webmaster@eide.es"
DEFAULT_REPLYTO_EMAIL = "no-reply@eide.es"

ACCOUNT_OPEN_SIGNUP = False
ACCOUNT_EMAIL_UNIQUE = False
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True

AUTHENTICATION_BACKENDS = [
    "account.auth_backends.UsernameAuthenticationBackend",
]

try:
    from local_settings import *
except ImportError:
    pass
          
