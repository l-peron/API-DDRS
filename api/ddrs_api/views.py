from curses.ascii import HT
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from ddrs_api.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class user_list(APIView):
    """
    List all Users
    """
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        utilisateurs = User.objects.all()
        serializer = UserSerializer(utilisateurs, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve data about a specific Utilisateur
    """
    try:
        utilisateur = User.objects.get(pk = pk)
    except User.DoesNotExist:
        return HttpResponse(status = 404)
    
    if request.method == 'GET':
        serializer = UserSerializer(utilisateur)
        return JsonResponse(serializer.data)

    # Error if not GET
    return HttpResponse(status = 400)