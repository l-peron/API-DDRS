from django.http import HttpResponse
from ddrs_api.models import User

def index(request):
    if request.user.is_authenticated:
        return HttpResponse('<p><p>You logged in as <strong>%s</strong>.</p><p><a href="/accounts/logout">Logout</a></p>' % request.user)
    else:
        return HttpResponse('<p><a href="/accounts/login">Login</a></p>')
