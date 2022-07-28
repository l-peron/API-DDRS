from curses.ascii import HT
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from rest_framework.views import APIView
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

class QuestionList(APIView):
    """
    List all Questions
    """

    types = [ QuestionSlider, QuestionLibre, QuestionChoixMultiple]
    serializers = [ QuestionSliderSerializer, QuestionLibreSerializer, QuestionChoixMultipleSerializer]
    names = [ 'slider', 'libre', 'qcm']

    def get(self, request, format=None):
        datas = {}
        for type, serial,name in zip(QuestionList.types, QuestionList.serializers, QuestionList.names):
            questions = type.objects.all()
            datas[name] = serial(questions, many=True).data
        # Merging
        return JsonResponse(datas, safe=False)

class QuestionListByType(APIView):
    """
    List all Questions or create new question by type
    """

    types = [ QuestionSlider, QuestionLibre, QuestionChoixMultiple]
    serializers = [ QuestionSliderSerializer, QuestionLibreSerializer, QuestionChoixMultipleSerializer]
    names = [ 'slider', 'libre', 'qcm']

    def get_tools(self, type):
        if type not in QuestionListByType.names:
            return HttpResponse(status = 404)
        i = QuestionListByType.names.index(type)
        return QuestionListByType.types[i], QuestionListByType.serializers[i]

    def get(self, request, type, format=None):
        model, serializer = self.get_tools(type)
        questions = model.objects.all()
        serialize = serializer(questions, many=True)
        return JsonResponse(serialize.data, safe=False)

    def post(self, request, type, format=None):
        entry_data = request.data
        serializer = self.get_tools(type)[1]
        serialize = serializer(data=entry_data)
        if serialize.is_valid():
            serialize.save()
            return JsonResponse(serialize.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    """
    Retrieve, update or delete a Question
    """
    types = [ QuestionSlider, QuestionLibre, QuestionChoixMultiple]
    serializers = [ QuestionSliderSerializer, QuestionLibreSerializer, QuestionChoixMultipleSerializer]
    names = [ 'slider', 'libre', 'qcm']

    def get_object(self, type, pk):
        i = QuestionDetail.names.index(type)
        try:
            return QuestionDetail.types[i].objects.get(pk = pk), QuestionDetail.serializers[i]
        except Snippet.DoesNotExist:
            raise HttpResponse(status = 404)

    def is_editable(self, question):
        questionnaire = Questionnaire.objects.get(pk = question.questionnaire_id)
        # Check if the related Questionnaire is on
        return not questionnaire.MONTHSTART_START <= datetime.now() <= questionnaire.MONTHSTART_END and not questionnaire.MONTHEND_START <= datetime.now() <= questionnaire.MONTHEND_END

    def get(self, request, type, pk, format=None):
        question, serial = self.get_object(type, pk)
        serializer = serial(question)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        if self.is_editable(question):
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
