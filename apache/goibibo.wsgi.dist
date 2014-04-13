import os, sys
sys.path.append('/home/ubuntu/work/')
sys.path.append('/home/ubuntu/work/motherusc')
sys.path.append('/home/ubuntu/work/motherusc/lib')
os.environ['DJANGO_SETTINGS_MODULE'] = 'motherusc.settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/ubuntu/work/motherusc/.python-eggs'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
