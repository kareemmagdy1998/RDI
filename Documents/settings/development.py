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
        "HOST": get_env_value("HOST_DEV"),
        "PORT": int(get_env_value("PORT")),
    }
}


