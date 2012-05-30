from django.conf.urls import patterns, include, url
from views import has_cert, index
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'cert/$', has_cert, ),
    url(r'^$', index, ),
)
