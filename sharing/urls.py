from django.conf.urls import url,patterns
from sharing.views import IndexView, PostView, LikeReportView

urlpatterns = patterns(
    "",
    url(r'post/(?P<post_id>\d+)/(?P<modus>[A-z]+)/',LikeReportView.as_view(), name="like"),
    url(r'^post/(?P<post_id>\d+)/', PostView.as_view(), name="post_details"),
    url(r"^$",IndexView.as_view(),name="index"),
)

