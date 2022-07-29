from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('ddrs_api.urls')),
]
