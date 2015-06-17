from django.conf.urls import url, patterns
from reservations.views import IndexView, CartView, CartConfirmView, CartDeleteView

urlpatterns = patterns(
    "",
    url(r'^addtocart/(?P<product_id>\d+)/', CartView.as_view(), name="addtocart"),
    url(r'^confirmcart/',CartConfirmView.as_view(), name="confirmcart"),
    url(r'^deletecart/',CartDeleteView.as_view(), name="deletecart"),
    url(r"^$", IndexView.as_view(), name="index"),
)