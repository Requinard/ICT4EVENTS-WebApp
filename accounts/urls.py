from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView.as_view(), name="logout"),

)