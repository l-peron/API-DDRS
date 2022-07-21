from django.contrib import admin
from django.urls import include, path
import django_cas_ng.views
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('', include('ddrs_api.urls')),
    path('accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
]