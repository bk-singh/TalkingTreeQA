import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.config.settings')

def pytest_configure():
    settings.DEBUG = False
    django.setup()