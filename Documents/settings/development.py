from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    "default": {
        "ENGINE": get_env_value("ENGINE"),
        "NAME": get_env_value("NAME"),
        "USER": get_env_value("USER"),
        "PASSWORD": get_env_value("PASSWORD"),
        "HOST": get_env_value("HOST"),
        "PORT": int(get_env_value("PORT")),
    }
}

# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

