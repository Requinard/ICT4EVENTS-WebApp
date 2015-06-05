from django.conf.urls import url,patterns
from sharing.views import IndexView, PostView

urlpatterns = patterns(
    "",
    url(r'^post/(?P<post_id>\d+)/', PostView.as_view(), name="post_detail"),
    url(r"^$",IndexView.as_view(),name="index"),
)

