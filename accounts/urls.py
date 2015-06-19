from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView.as_view(), name="logout"),
    url(r'^new/', CreateNewAccountView.as_view(), name="create"),
    url(r'^profile/set/(?P<mode>\w+)/', ProfileView.as_view(), name="profile-set"),
    url(r'^profile/(?P<username>\w+)/', ProfileView.as_view(), name="profile-user"),
    url(r'^activate/(?P<hashcode>\d+)/', ActivateView.as_view(), name="activate"),
    url(r'^$', ProfileView.as_view(), name="profile"),
)
