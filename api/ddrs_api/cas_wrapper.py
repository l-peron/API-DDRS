from django.views import View
from django_cas_ng import views as cas_views
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from rest_framework_jwt.settings import api_settings

from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class APILoginView(cas_views.LoginView):
    def successful_login(self, request: HttpRequest, next_page: str) -> HttpResponse:
        return HttpResponseRedirect('/getToken/')

class getToken(View):
    def get(self, request : HttpRequest):
        if request.user.is_authenticated:
            user = request.user
            # payload = JWT_PAYLOAD_HANDLER(user)
            # token = JWT_ENCODE_HANDLER(payload)
            refresh = RefreshToken.for_user(user)

            print(user.is_superuser)

            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, safe = False)
        else:
            return HttpResponse(status = 401)