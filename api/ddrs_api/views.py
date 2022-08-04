from curses.ascii import HT
import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from ddrs_api.serializers import QuestionnaireSerializer, UserSerializer
from rest_framework.views import APIView

from django.contrib.auth.models import User
from ddrs_api.models import Questionnaire, Question
from ddrs_api.models import QuestionSlider, QuestionChoixMultiple, QuestionLibre
from ddrs_api.models import ReponseSlider, ReponseChoixMultiple, ReponseLibre
from ddrs_api.models import User, RCMChamp, QCMChamp

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
    }
    """
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        # user_id = request.POST.get('user_id')
        answer_text = request.POST.get('answer_text')

        # user = User.objects.get(pk=user_id)

        try:
            existing_entry = ReponseLibre.objects.get(question=question_id) # user=user
            if existing_entry:
                existing_entry.answer_text = answer_text
                existing_entry.save()
                # Not sure if the user should be redirected or if it should just return a flag to indicate whether or not the query was successful
                return HttpResponse(status=201)
        except ReponseLibre.DoesNotExist:
            question = QuestionLibre.objects.get(pk=question_id)
            new_entry = ReponseLibre(answer_date=answer_date, answer_text=answer_text, question=question)
            new_entry.save()
            # Same here
            return HttpResponse(status=201)
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
    }
    """
    if request.method == 'POST':
        # the request should contain all the following fields: answer_date, answer_value, question_id, user_id
        question_id = request.POST.get('question_id')
        # user_id = request.POST.get('user_id')
        answer_value = int(request.POST.get('answer_value'))

        # user = User.objects.get(pk=user_id)

        question = QuestionSlider.objects.get(pk=question_id)
        min_value, max_value = question.value_min, question.value_max

        if answer_value not in list(range(min_value, max_value + 1)):
            return HttpResponse(status=400, reason=f"Value {answer_value} is out of allowed range({min_value}-{max_value})")

        try:
            existing_entry = ReponseSlider.objects.get(question=question_id)# user=user
            if existing_entry:
                existing_entry.answer_value = answer_value
                existing_entry.save()
                # Not sure if the user should be redirected or if it should just return a flag to indicate whether or not the query was successful
                return HttpResponse(status=201)
        except ReponseSlider.DoesNotExist:
            new_entry = ReponseSlider(answer_value=answer_value, question=question)
            new_entry.save()
            # Same here
            return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def reponse_qcm(request):
    """
    Requests are (for now) thought to be formatted like so:
    data={
        user_id: int,
        question_id: int,
        selected_fields: list of IDs (i.e.: [1,3,4])
    }
    """
    question_id = request.POST.get('question_id')
    selected_fields = eval(request.POST.get('selected_fields'))

    question = QuestionChoixMultiple.objects.get(pk=question_id)
    all_fields = [field.pk for field in question.qcmchamp_set.all()]
    try:
        existing_answer = ReponseChoixMultiple.objects.get(question=question_id) # user=user
        linked_rcmchamps = existing_answer.rcmchamp_set.all()
        if linked_rcmchamps:
            for field in linked_rcmchamps:
                field.checked_boolean = field.qcmchamp.pk in selected_fields
                field.save()
        else:
            for field_id in all_fields:
                qcmchamp = QCMChamp.objects.get(pk=field_id)
                answer_bool = field_id in selected_fields
                new_answer_field = RCMChamp(checked_boolean=answer_bool, rcm=existing_answer, qcmchamp=qcmchamp)
                new_answer_field.save()
        # Update 'last modified' date of answer
        existing_answer.save()
        return HttpResponse(status=201)
    except ReponseChoixMultiple.DoesNotExist:
        new_entry = ReponseChoixMultiple(question=question)
        new_entry.save()
        for field in all_fields:
            qcmchamp = QCMChamp.objects.get(pk=field)
            answer_bool = field.pk in selected_fields
            new_answer_field = RCMChamp(checked_boolean=answer_bool, rcm=new_entry, qcmchamp=qcmchamp)
            new_answer_field.save()
        # Same here
        return HttpResponse(status=201)
