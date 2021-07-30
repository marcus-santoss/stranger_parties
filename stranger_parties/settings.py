import datetime
import os
from pathlib import Path

import environ

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = env("DEBUG", cast=bool)
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = ["0.0.0.0"]

# ======================[ APPS ]==============================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "corsheaders",
    "rest_framework",
    "drf_yasg2",
    "django_filters",
    "stranger_parties.core",
    "stranger_parties.invite",
]

# ======================[ MIDDLEWARE ]=======================================
MIDDLEWARE = [
    # "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# ======================[ ROOT URL ]==========================================
ROOT_URLCONF = "stranger_parties.urls"

# ======================[ TEMPLATES ]==========================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# ======================[ WSGI OBJECT ]======================================
WSGI_APPLICATION = "stranger_parties.wsgi.application"

# ======================[ DATABASES ]=========================================
DATABASES = {"default": env.db()}

# ==================[ CORS ]===================================
# CORS_ORIGIN_ALLOW_ALL = True

# ======================[ EMAIL ] ============================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "0.0.0.0"
EMAIL_PORT = "1025"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

# ======================[ AUTH_PASSWORD_VALIDATORS ] =========================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ======================[ DEFAULT PRIMARY KEY FIELD TYPE ]=================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "core.User"

# ======================[ INTERNATIONALIZATION ]============================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ======================[ STATIC / MEDIA ]=================================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_DIRS = (os.path.join(BASE_DIR, "staticfiles"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_DIRS = (os.path.join(BASE_DIR, "mediafiles"),)

# ======================[ JWT ] ===========================================
JWT_AUTH = {"JWT_EXPIRATION_DELTA": datetime.timedelta(minutes=60)}

# ======================[ REST FRAMEWORK ]=================================
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication"
    ],
}

# ======================[ SWAGGER ]======================
SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "stranger_parties.urls.open_api_obj",
    "SECURITY_DEFINITIONS": {
        "JWT": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
}
