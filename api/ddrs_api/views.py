from curses.ascii import HT
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from ddrs_api.models import Utilisateur
from ddrs_api.serializers import UtilisateurSerializer

@csrf_exempt
def user_list(request):
    """
    List all Utilisateurs
    """
    if request.method == 'GET':
        utilisateurs = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(utilisateurs, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    # Error if not GET
    return HttpResponse(status = 400)

@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve data about a specific Utilisateur
    """
    try:
        utilisateur = Utilisateur.objects.get(pk = pk)
    except Utilisateur.DoesNotExist:
        return HttpResponse(status = 404)
    
    if request.method == 'GET':
        serializer = UtilisateurSerializer(utilisateur)
        return JsonResponse(serializer.data)

    # Error if not GET
    return HttpResponse(status = 400)