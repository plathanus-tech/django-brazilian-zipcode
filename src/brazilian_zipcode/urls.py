from django.urls import path, include


urlpatterns = [path("api/", include("brazilian_zipcode.api.urls"))]
