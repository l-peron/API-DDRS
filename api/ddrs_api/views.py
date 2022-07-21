from curses.ascii import HT
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from ddrs_api.models import User
from ddrs_api.serializers import UserSerializer

@csrf_exempt
def user_list(request):
    """
    List all users
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    # Error if not GET
    return HttpResponse(status = 400)

@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve data about a specific user
    """
    try:
        user = User.objects.get(pk = pk)
    except User.DoesNotExist:
        return HttpResponse(status = 404)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    # Error if not GET
    return HttpResponse(status = 400)