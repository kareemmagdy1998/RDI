import os
import django
from pytest import fixture

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Documents.settings.development")

django.setup()

@fixture(autouse=True)
def enable_db_access(db):
    """Enable database access for all tests."""
    pass
