from curses.ascii import HT
import json
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from ddrs_api.serializers import QuestionLibreSerializer, QuestionnaireSerializer, RCMChampSerializer, ReponseChoixMultipleSerializer, ReponseLibreSerializer, ReponseSliderSerializer, UserSerializer
from rest_framework.views import APIView

from django.contrib.auth.models import User
from ddrs_api.models import Questionnaire, Question
from ddrs_api.models import QuestionSlider, QuestionChoixMultiple, QuestionLibre
from ddrs_api.models import ReponseSlider, ReponseChoixMultiple, ReponseLibre
from ddrs_api.models import User, RCMChamp, QCMChamp

# USERS

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

# QUESTIONNAIRES

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

# REPONSES (GENERAL)

class reponse_list(APIView):

    types = [ ReponseSlider, ReponseLibre, ReponseChoixMultiple]
    serializers = [ ReponseSliderSerializer, ReponseLibreSerializer, ReponseChoixMultipleSerializer ]
    names = [ 'slider', 'libre' , 'qcm' ]

    def get(self, request, format=None):
        """
        List all Reponse
        """
        datas = {}
        for type, serial,name in zip(reponse_list.types, reponse_list.serializers, reponse_list.names):
            questions = type.objects.all()
            datas[name] = serial(questions, many=True).data
        # Merging
        return JsonResponse(datas, safe=False)

class reponse_detail(APIView):
    types = [ ReponseSlider, ReponseLibre, ReponseChoixMultiple]
    serializers = [ ReponseSliderSerializer, ReponseLibreSerializer, ReponseChoixMultipleSerializer ]
    names = [ 'slider', 'libre' , 'qcm' ]

    def get_object(self, type, pk):
        i = reponse_detail.names.index(type)
        try:
            return reponse_detail.types[i].objects.get(pk = pk), reponse_detail.serializers[i]
        except reponse_detail.types[i].DoesNotExist:
            return None

    def get(self, request, type, pk):
        if not self.get_object(type, pk):
            return HttpResponse(status=404)
        question, serializer = self.get_object(type, pk)
        serialize = serializer(question)
        return JsonResponse(serialize.data, safe=False)

# REPONSES LIBRES

class reponse_libre_list(APIView):
    def get(self, request):
        """
        List all Reponse Libre
        """
        reponses = ReponseLibre.objects.all()
        serializer = ReponseLibreSerializer(reponses, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        """
        Creates (doesn't update) a reponse libre
        """
        post_data = request.data
        # when JWT is merged it will be
        # user = request.user
        # for now we put the user in the request

        try:
            user_id = post_data['user_id']
            # If entry already exists -> error :
            # updates are meant to be made via PUT
            ReponseLibre.objects.get(question_id = post_data['question_id'], user_id = user_id) # user=user
            return HttpResponse(status = 400, reason = "Duplicate question")
        except ReponseLibre.DoesNotExist:
            # Else we create a new entry
            try:
                serializer = ReponseLibreSerializer(data = post_data)
                if serializer.is_valid(raise_exception = True):
                    serializer.save()
                    return HttpResponse(status = 201)
                # 400 Bad Request
                return HttpResponse(status = 400)
            except IntegrityError:
                # Integrity of db is not respected (unknown fk, null value,...)
                # 400 Bad Request
                return HttpResponse(status = 400)
        except KeyError:
            # 400 Bad Request
            return HttpResponse(status = 400)

# REPONSES SLIDERS

class reponse_slider_list(APIView):
    def get(self, request):
        """
        List all Reponse Slider
        """
        reponses = ReponseSlider.objects.all()
        serializer = ReponseSliderSerializer(reponses, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        """
        Creates (doesn't update) a reponse slider
        """
        post_data = request.data
        # when JWT is merged it will be
        # user = request.user
        # for now we put the user in the request

        try:
            question = QuestionSlider.objects.get(pk=post_data['question_id'])
            min_value, max_value = question.value_min, question.value_max

            answer_value = post_data['answer_value']

            if answer_value not in list(range(min_value, max_value + 1)):
                return HttpResponse(status=400, reason=f"Value {answer_value} is out of allowed range({min_value}-{max_value})")

            user_id = post_data['user_id']

            # If entry already exists -> error :
            # updates are meant to be made via PUT
            ReponseSlider.objects.get(question_id = post_data['question_id'], user_id = user_id) # user=user
            return HttpResponse(status = 400, reason = "Duplicate question")
        except QuestionSlider.DoesNotExist:
            # 404 Not Found
            return HttpResponse(status = 404, reason = f"Question with id {post_data['question_id']} not found")
        except ReponseSlider.DoesNotExist:
            # Else we create a new entry
            try:
                serializer = ReponseSliderSerializer(data = post_data)
                if serializer.is_valid(raise_exception = True):
                    serializer.save()
                    return HttpResponse(status = 201)
                # 400 Bad Request
                return HttpResponse(status = 400)
            except IntegrityError:
                # Integrity of db is not respected (unknown fk, null value,...)
                # 400 Bad Request
                return HttpResponse(status = 400)
        except KeyError:
            # 400 Bad Request
            return HttpResponse(status = 400)

# REPONSES QCM

class reponse_qcm_list(APIView):
    def get(self, request):
        """
        List all Reponse Slider
        """
        reponses = ReponseChoixMultiple.objects.all()
        serializer = ReponseChoixMultipleSerializer(reponses, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        """
        Creates (doesn't update) a reponse slider
        """

        post_data = request.data

        # when JWT is merged it will be
        # user = request.user
        # for now we put the user in the request

        """
        Requests are (for now) thought to be formatted like so:
        data={
            user_id: int,
            question_id: int,
            selected_fields_ids: list of IDs (i.e.: [1,32,4])
        }
        """
        try:
            user_id = post_data['user_id']

            # If entry already exists -> error :
            # updates are meant to be made via PUT
            ReponseChoixMultiple.objects.get(question_id = post_data['question_id'], user_id = user_id) # user=user
            return HttpResponse(status = 400, reason = "Duplicate question")
        except ReponseChoixMultiple.DoesNotExist:
            # Else we create a new entry
            try:
                
                serializer = ReponseChoixMultipleSerializer(data = post_data)
                if serializer.is_valid(raise_exception = True):
                    rcm_id = serializer.save().id
                    
                    selected_fields = post_data['selected_fields_ids']

                    # For every selected answer
                    for id in selected_fields:
                        # Create a serializer for a RCMChamp
                        field_serializer = RCMChampSerializer(
                            data = {
                                'rcm_id' : rcm_id, 
                                'qcmchamp_id': id
                                }
                            )
                        # Check if valid
                        if field_serializer.is_valid():
                            field_serializer.save()

                    return HttpResponse(status = 201)
                # 400 Bad Request
                return HttpResponse(status = 400)
            except IntegrityError:
                # Integrity of db is not respected (unknown fk, null value,...)
                # 400 Bad Request
                return HttpResponse(status = 400)
        except KeyError:
            return HttpResponse(status = 400)
