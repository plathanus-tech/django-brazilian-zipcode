from django.urls import path, include


urlpatterns = [path("api/", include("brazilian_address.api.urls"))]
