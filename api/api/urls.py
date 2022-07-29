from django.contrib import admin
from django.urls import include, path
import django_cas_ng.views
from ddrs_api.cas_wrapper import APILoginView, getToken
from . import views

from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('', views.index, name = 'index'),
    path('', include('ddrs_api.urls')),
        path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('getToken', getToken.as_view(), name="get_token"),
    path('accounts/login', APILoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
]