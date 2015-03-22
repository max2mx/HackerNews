from django.conf.urls import patterns, include, url


import autocomplete_light
autocomplete_light.autodiscover()
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    #
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'', include('feed.urls', 'feed')),
    url(r'^accounts/', include('registration.urls')),
)
