from django.contrib import admin
from django.urls import include, path
import django_cas_ng.views
from ddrs_api.cas_wrapper import APILoginView, getToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', include('ddrs_api.urls')),
    path('admin/', admin.site.urls),
    path('getToken/', getToken.as_view(), name="get_token"),
    path('refreshToken/', TokenRefreshView.as_view(), name="refresh_view"),
    path('login/', APILoginView.as_view(), name='cas_ng_login'),
    path('logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
]