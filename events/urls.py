from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',
    url(r'^event/set/(?P<event_id>\d+)/', SetActiveEventView.as_view(), name="set_active_event"),
    url(r'^event/(?P<event_id>\d+)/', EventDetailsView.as_view(), name="details"),
    url(r'^search/(?P<query>[A-z0-9+]+)', SearchView.as_view(), name="search"),
    url(r'^$', IndexView.as_view(), name="index"),
)