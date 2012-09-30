from django.conf.urls import patterns, include, url
from views import cert, index, curriculum, certificate
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'cert/$', cert, ),
    url(r'curriculum/(?P<pk>.*)/$', curriculum,),
    url(r'certificate/(?P<pk>.*)/$', certificate,),
    url(r'^$', index,),
)
