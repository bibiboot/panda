import settings
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

PROJECT_PATH = settings.PROJECT_PATH
STATIC_PATH = settings.PROJECT_PATH + "/"

urlpatterns = patterns('',

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
   
   (r'^$', 'panda.events.views.home'),
   (r'^homenext/', 'panda.events.views.homenext'),

   (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_PATH +'html/css/'}),
   (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_PATH + 'html/js/'}),
   (r'^html/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_PATH + 'html/templates/'}),
   (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_PATH + 'html/images/'}),
   (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_PATH + 'django_facebook/static/'}),

   (r'^favicon\.ico/$', 'django.views.generic.simple.redirect_to', {'url': 'http://'+settings.HOST+'/images/favicon.ico'}),
)
