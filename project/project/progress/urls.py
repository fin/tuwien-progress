from django.conf.urls import patterns, include, url
from views import has_cert

urlpatterns = patterns('',
    url(r'cert/', has_cert, ),
)
