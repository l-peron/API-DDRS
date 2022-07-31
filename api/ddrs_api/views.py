from curses.ascii import HT
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ddrs_api.serializers import QuestionnaireSerializer, UserSerializer
from rest_framework.views import APIView

from django.contrib.auth.models import User
from ddrs_api.models import Questionnaire, Question
from ddrs_api.models import QuestionSlider, QuestionChoixMultiple, QuestionLibre
from ddrs_api.models import ReponseSlider, ReponseChoixMultiple, ReponseLibre
from ddrs_api.models import User, RCMChamp


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

@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve data about a specific Utilisateur
    """
    try:
        utilisateur = User.objects.get(pk = pk)
    except User.DoesNotExist:
        return HttpResponse(status = 404)

    return render(request, 'ddrs_api/detail.html', {'questions': questions})
    

    if request.method == 'GET':
        serializer = UserSerializer(utilisateur)
        return JsonResponse(serializer.data)

    # Error if not GET
    return HttpResponse(status = 400)

@csrf_exempt
def reponse_libre(request):
    """
    Requests are (for now) thought to be formatted like so:
    data={
        user_id: int,
        question_id: int,
        answer_text: string,
        answer_date: "XX/XX/XXXX"
    }
    """
    # the request should contain all the following fields: answer_date, answer_text, question_id, user_id
    # return JsonResponse(request.POST)
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_id = request.POST.get('user_id')
        answer_text = request.POST.get('answer_text')
        answer_date = request.POST.get('answer_date')

        user = User.objects.get(pk=user_id)

        try:
            existing_entry = ReponseLibre.objects.get(question=question_id, user=user_id)
            if existing_entry:
                existing_entry.answer_text = answer_text
                existing_entry.save()
                # Not sure about if the user should be redirected or if it should just return a flag to indicate whether or not the query was successful
                return HttpResponseRedirect(reverse('questionnaire'))
        except ReponseLibre.DoesNotExist:
            new_entry = ReponseLibre(answer_date=answer_date, user=user_id, answer_text=answer_text, question=question_id)
            new_entry.save()
            # Same here
            return HttpResponseRedirect(reverse('questionnaire'))
    else:
        return HttpResponse(status=400)

@csrf_exempt
def reponse_slider(request):
    """
    Requests are (for now) thought to be formatted like so:
    data={
        user_id: int,
        question_id: int,
        answer_value: int,
        answer_date: "XX/XX/XXXX"
    }
    """
    if request.method == 'POST':
        # the request should contain all the following fields: answer_date, answer_value, question_id, user_id
        question_id = request.POST.get('question_id')
        user_id = request.POST.get('user_id')
        answer_value = request.POST.get('answer_value')
        answer_date = request.POST.get('answer_date')

        user = User.objects.get(pk=user_id)

        try:
            existing_entry = ReponseSlider.objects.get(question=question_id, user=user_id)
            if existing_entry:
                existing_entry.answer_value = answer_value
                existing_entry.save()
                # Not sure about if the user should be redirected or if it should just return a flag to indicate whether or not the query was successful
                return HttpResponseRedirect(reverse('questionnaire'))
        except ReponseSlider.DoesNotExist:
            new_entry = ReponseSlider(answer_date=answer_date, user=user, answer_value=answer_value, question=question_id)
            new_entry.save()
            # Same here
            return HttpResponseRedirect(reverse('questionnaire'))
    else:
        return HttpResponse(status=400)

@csrf_exempt
def reponse_qcm(request):
    # TODO
    pass
