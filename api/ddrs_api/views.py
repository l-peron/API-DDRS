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
    def post(self, request):
        utilisateurs = User.objects.all()
        serializer = UserSerializer(utilisateurs, many=True)
        return JsonResponse(serializer.data, safe=False)

class user_detail(APIView):
    def post(self, request, *args, **kwargs):
        """
        Retrieve data about a specific Utilisateur
        """
        try:
            utilisateur = User.objects.get(pk = kwargs['pk'])
        except User.DoesNotExist:
            return HttpResponse(status = 404)

        serializer = UserSerializer(utilisateur)
        return JsonResponse(serializer.data)
    