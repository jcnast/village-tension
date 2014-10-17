from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from characters import views

# extends ^character/
character_urls = patterns('$',
	url(r'test/$', views.test),
)