import os, sys
sys.path.append('/home/work/')
sys.path.append('/home/work/pand')
sys.path.append('/home/work/panda/lib')
os.environ['DJANGO_SETTINGS_MODULE'] = 'panda.settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/work/panda/.python-eggs'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
