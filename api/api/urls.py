from django.contrib import admin
from django.urls import include, path
import django_cas_ng.views
from ddrs_api.cas_wrapper import APILoginView, getToken

urlpatterns = [
    path('', include('ddrs_api.urls')),
    path('getToken/', getToken.as_view(), name="get_token"),
    path('login/', APILoginView.as_view(), name='cas_ng_login'),
    path('logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
]