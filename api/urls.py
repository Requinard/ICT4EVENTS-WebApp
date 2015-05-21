from django.conf.urls import url, patterns, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = patterns(
    '',
    url(r'^api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),router
)