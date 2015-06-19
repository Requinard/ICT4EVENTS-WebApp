from django.conf.urls import url, patterns

from staff.views import IndexView, GenerateView

urlpatterns = patterns(
    '',
    url(r'^generate/', GenerateView.as_view(), name="generate"),
    url(r'^$', IndexView.as_view(), name="index"),
)
