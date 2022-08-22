import json
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from ddrs_api.models import Questionnaire, QuestionChoixMultiple, QuestionSlider, QuestionLibre
from ddrs_api.serializers import QuestionnaireSerializer, QuestionChoixMultipleSerializer, QuestionSliderSerializer, QuestionLibreSerializer, QCMChampSerializer

class questionnaires_list(APIView):
    def get(self, request):
        """
        List all Questionnaires
        """
        questionnaires = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        """
        Creates a Questionnaire with received fields and return its informations
        
        Infos are received following this format :
        {
            'title_text' : String,
            'MONTHSTART_START' : Date,
            'MONTHSTART_END' : Date,
            'MONTHEND_START' : Date,
            'MONTHEND_END' : Date
        }
        """
        post_data = json.loads(request.body)

        try:
            questionnaire = Questionnaire(
                title_text = post_data['title_text'], 
                MONTHSTART_START = post_data['MONTHSTART_START'],
                MONTHSTART_END = post_data['MONTHSTART_END'],
                MONTHEND_START = post_data['MONTHEND_START'],
                MONTHEND_END = post_data['MONTHEND_END']
            )

            questionnaire.save()
            serializer = QuestionnaireSerializer(questionnaire)
            
            return JsonResponse(serializer.data)
        except KeyError:
            # 400 Bad Request
            return HttpResponse(status = 400)

class questionnaire_detail(APIView):
    def get(self, request, *args, **kwargs):
        """
        Retrieve data about a specific Questionnaire
        """
        try:
            questionnaire = Questionnaire.objects.get(pk = kwargs['pk'])
        except Questionnaire.DoesNotExist:
            return HttpResponse(status = 404)
        
        serializer = QuestionnaireSerializer(questionnaire)
        return JsonResponse(serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Delete a specific Questionnaire
        """
        try:
            questionnaire = Questionnaire.objects.get(pk = kwargs['pk'])
        except Questionnaire.DoesNotExist:
            return HttpResponse(status = 404)

        questionnaire.delete()
        return HttpResponse(status = 200)

class QuestionList(APIView):
    """
    List all Questions
    """

    types = [QuestionSlider, QuestionLibre, QuestionChoixMultiple]
    serializers = [QuestionSliderSerializer, QuestionLibreSerializer, QuestionChoixMultipleSerializer]
    names = ['slider', 'libre', 'qcm']

    def get(self, request, format=None):
        datas = {}
        for type, serial, name in zip(QuestionList.types, QuestionList.serializers, QuestionList.names):
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
        i = QuestionListByType.names.index(type)
        return QuestionListByType.types[i], QuestionListByType.serializers[i]

    def is_addable(self, questionnaire_id):
        questionnaire = Questionnaire.objects.get(pk = questionnaire_id)
        # Check if the related Questionnaire is on
        return not questionnaire.MONTHSTART_START <= timezone.now() <= questionnaire.MONTHSTART_END and not questionnaire.MONTHEND_START <= timezone.now() <= questionnaire.MONTHEND_END

    def get(self, request, type, format=None):
        if type not in QuestionListByType.names:
            return HttpResponse(status = 404)
        model, serializer = self.get_tools(type)
        questions = model.objects.all()
        serialize = serializer(questions, many=True)
        return JsonResponse(serialize.data, safe=False)

    def post(self, request, type, format=None):
        if type not in QuestionListByType.names:
            return HttpResponse(status = 404)
        entry_data = request.data
        serializer = self.get_tools(type)[1]
        serialize = serializer(data=entry_data)
        if serialize.is_valid() and self.is_addable(entry_data["questionnaire_id"]):
            serialize.save()
            if type == "qcm":
                return self.post_qcm(entry_data["champs"], serialize.data["id"])
            return HttpResponse(status=201)
        return HttpResponse(status=400)

    def post_qcm(self, datas, question_id):
        entry_data = {}
        for title in datas:
            entry_data["title_text"] = title
            entry_data["question_id"] = question_id
            serialize = QCMChampSerializer(data=entry_data)
            if serialize.is_valid():
                serialize.save()
            else:
                return HttpResponse(status=400)
        return HttpResponse(status=201)


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
        except QuestionDetail.types[i].DoesNotExist:
            return None

    def is_editable(self, fk_id):
        questionnaire = Questionnaire.objects.get(pk = 2)
        # Check if the related Questionnaire is on
        return not questionnaire.MONTHSTART_START <= timezone.now() <= questionnaire.MONTHSTART_END and not questionnaire.MONTHEND_START <= timezone.now() <= questionnaire.MONTHEND_END

    def get(self, request, type, pk):
        if not self.get_object(type, pk):
            return HttpResponse(status=404)
        question, serializer = self.get_object(type, pk)
        serialize = serializer(question)
        return JsonResponse(serialize.data, safe=False)

    def delete(self, request, type, pk):
        if not self.get_object(type, pk):
            return HttpResponse(status=404)
        question = self.get_object(type, pk)[0]
        if self.is_editable(question.questionnaire_id):
            question.delete()
            return HttpResponse(status=204)

    def patch(self, request, type, pk):
        if not self.get_object(type, pk):
            return HttpResponse(status=404)
        question, serializer = self.get_object(type, pk)
        serialize = serializer(question, data=request.data, partial=True)
        if serialize.is_valid():
            serialize.save()
            return JsonResponse(code=201, data=serialize.data, safe=False)
        return JsonResponse(code=400, data="wrong parameters")
