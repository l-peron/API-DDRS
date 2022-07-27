from curses.ascii import HT
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ddrs_api.models import Questionnaire
from ddrs_api.serializers import QuestionnaireSerializer

@csrf_exempt
def questionnaires_list(request):
    """
    List all Questionnaires
    """
    if request.method == 'GET':
        questionnaires = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    # Error if not GET
    return HttpResponse(status = 400)

@csrf_exempt
def questionnaire_detail(request, pk):
    """
    Retrieve data about a specific Questionnaire
    """
    try:
        questionnaire = Questionnaire.objects.get(pk = pk)
    except Questionnaire.DoesNotExist:
        return HttpResponse(status = 404)
    
    if request.method == 'GET':
        serializer = QuestionnaireSerializer(questionnaire)
        return JsonResponse(serializer.data)

    # Error if not GET
    return HttpResponse(status = 400)