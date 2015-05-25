from django.conf.urls import url, patterns, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()


urlpatterns = patterns(
    '',
    url(r'^api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auto/plek/(?P<name>\w+)/', PlekAutocompleteViewset.as_view()),
    url(r'^', include(router.urls)),router
)