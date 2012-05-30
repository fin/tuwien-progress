from django.conf.urls import patterns, include, url
from views import has_cert, index

urlpatterns = patterns('',
    url(r'cert/', has_cert, ),
    url(r'^$', index, ),
)
