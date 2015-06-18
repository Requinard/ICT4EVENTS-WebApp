from django.conf.urls import url, patterns
from reservations.views import IndexView, CartView, CartConfirmView, CartDeleteView,PlaceReservationView, PlaceAddnewPerson

urlpatterns = patterns(
    "",
    url(r'^cart/add/(?P<product_id>\d+)/', CartView.as_view(), name="addtocart"),
    url(r'^cart/confirm/',CartConfirmView.as_view(), name="confirmcart"),
    url(r'^cart/delete/',CartDeleteView.as_view(), name="deletecart"),
    url(r'^place/new/(?P<place_id>\d+)/', PlaceAddnewPerson.as_view(), name="place_add"),
    url(r'^place/', PlaceReservationView.as_view(), name="place"),
    url(r"^$", IndexView.as_view(), name="index"),
)