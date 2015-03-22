from django.conf.urls import patterns, include, url
import ragbackend 
from registration.backends.default.views import RegistrationView
from forms import UserRegForm
import autocomplete_light
autocomplete_light.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'feed.views.index', name='index'),
    url(r'^story/$', 'feed.views.story', name='story'),
    url(r'^feed/$', 'feed.views.feed', name='feed'),
    url(r'^feeds/$', 'feed.views.feeds', name='feeds'),
    url(r'^story/(?P<story_id>\d+)/$', 'feed.views.story_detail', name='story_detail'),
    url(r'^vote/$', 'feed.views.vote', name='vote'),
    url(r'^register/$', RegistrationView.as_view(form_class=UserRegForm)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)

