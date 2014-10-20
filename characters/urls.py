from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from characters import views

# extends ^character/
character_urls = patterns('$',

	url(r'test/$', views.test),
	url(r'default-people/$', views.default_people),
	url(r'default-opinions/$', views.default_opinions),
	url(r'default-relations/$', views.default_relations),
	url(r'interaction/(?P<aquaintance>.*)/(?P<character>.*)/(?P<care>.*)/(?P<impact>.*)/$', views.interaction),

)