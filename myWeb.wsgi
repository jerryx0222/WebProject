import os
import sys

sys.path.append('/home/intai/myWeb/WebProject')
os.environ['DJANGO_SETTINGS_MODULE']='WebProject.settings.py'

from django.core.wsgi import get_wsgi.application
application = get_wsgi_application()
