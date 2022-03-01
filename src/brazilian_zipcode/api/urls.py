from django.urls import path
from . import views


urlpatterns = [
    path("address_info", views.address_info, name="address_info"),
]
