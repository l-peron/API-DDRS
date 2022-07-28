from curses.ascii import HT
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ddrs_api.models import Questionnaire
from ddrs_api.models import Question, QuestionChoixMultiple, QuestionSlider, QuestionLibre
from ddrs_api.serializers import QuestionnaireSerializer
from ddrs_api.serializers import QuestionChoixMultipleSerializer, QuestionSliderSerializer, QuestionLibreSerializer

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

@csrf_exempt
def questions_list(request):
    """
    List all Questions
    """
    if request.method == 'GET':

        datas = {}
        types = [ QuestionSlider, QuestionLibre, QuestionChoixMultiple]
        serializers = [ QuestionSliderSerializer, QuestionLibreSerializer, QuestionChoixMultipleSerializer]
        names = [ 'sliders', 'libre', 'qcms']

        for type, serial,name in zip(types, serializers, names):
            questions = type.objects.all()
            datas[name] = serial(questions, many=True).data

        # Merging
        return JsonResponse(datas, safe=False)

    # Error if not GET
    return HttpResponse(status = 400)

@csrf_exempt
def question_detail(request, pk):
    """
    Retrieve data about a specific Question
    """
    types = [ QuestionSlider, QuestionLibre, QuestionChoixMultiple]
    serializers = [ QuestionSliderSerializer, QuestionLibreSerializer, QuestionChoixMultipleSerializer]

    if request.method == 'GET':
        for type, serial in zip(types, serializers):
            try:
                question = type.objects.get(pk = pk)
                serializer = serial(question)
                return JsonResponse(serializer.data, safe=False)
            except type.DoesNotExist:
                continue
        return HttpResponse(status = 404)

    # Error if not GET
    return HttpResponse(status = 400)
