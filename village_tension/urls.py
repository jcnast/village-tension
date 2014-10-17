from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from characters.urls import character_urls
from village_tension import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'village_tension.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^character/', include(character_urls)),

    # how to import Dad's soundcloud
    url(r'^soundcloud/$', views.soundcloud),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)