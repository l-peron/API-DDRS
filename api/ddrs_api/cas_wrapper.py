from django.views import View
from django_cas_ng import views as cas_views
from django_cas_ng.models import ProxyGrantingTicket, SessionTicket
from django_cas_ng.utils import get_protocol, get_redirect_url, get_cas_client
from django_cas_ng.signals import cas_user_logout
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from urllib import parse as urllib_parse
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from .models import User


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class APILoginView(cas_views.LoginView):
    def successful_login(self, request: HttpRequest, next_page: str) -> HttpResponse:
        """
        This method is called on successful login.
        Overriden to render a page that send JWT token via postMessage
        if the page receive a message from one of the whitelisted origin.
        """
        user = request.user
        payload = JWT_PAYLOAD_HANDLER(user)
        token = JWT_ENCODE_HANDLER(payload)

        data = {
            "token": token,
            # "cors_origin_regex_whitelist": settings.CORS_ALLOWED_ORIGINS,
            "next_page": next_page,
        }

        return JsonResponse(data, safe = False)

class getToken(View):
    def get(self, request : HttpRequest):
        user = request.user
        payload = JWT_PAYLOAD_HANDLER(user)
        token = JWT_ENCODE_HANDLER(payload)

        data = {
            "token": token,
        }

        return JsonResponse(data, safe = False)