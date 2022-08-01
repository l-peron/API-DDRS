from curses.ascii import HT
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ddrs_api.models import Questionnaire
from ddrs_api.serializers import QuestionnaireSerializer
from rest_framework.views import APIView

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
