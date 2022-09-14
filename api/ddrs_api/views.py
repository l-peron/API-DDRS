from curses.ascii import HT
import json
from sys import stderr
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from ddrs_api.serializers import QuestionLibreSerializer, QuestionnaireSerializer, RCMChampSerializer, ReponseChoixMultipleSerializer, ReponseLibreSerializer, ReponseSliderSerializer, UserSerializer, QuestionSliderSerializer, QuestionChoixMultipleSerializer
from rest_framework.views import APIView

from django.contrib.auth.models import User
from ddrs_api.models import Questionnaire, Question
from ddrs_api.models import QuestionSlider, QuestionChoixMultiple, QuestionLibre
from ddrs_api.models import ReponseSlider, ReponseChoixMultiple, ReponseLibre
from ddrs_api.models import User, RCMChamp, QCMChamp

from rest_framework.permissions import IsAuthenticated

# USERS

class user_list(APIView):
    """
    List all Users
    """
    
    def get(self, request):
        utilisateurs = User.objects.all()
        serializer = UserSerializer(utilisateurs, many=True)
        return JsonResponse(serializer.data, safe=False)

class user_detail(APIView):
    def get(self, request, *args, **kwargs):
        """
        Retrieve data about a specific Utilisateur
        """

        # Check if user is either admin, or the request concern the user
        user_id = kwargs['pk']

        if not (request.user.is_superuser or request.user.id == user_id):
            print(f"{user_id} is not {request.user.id} nor admin.", file=stderr)
            # Unauthorized
            return HttpResponse(status = 401)

        try:
            utilisateur = User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return HttpResponse(status = 404)

        serializer = UserSerializer(utilisateur)
        return JsonResponse(serializer.data)

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
        user_id = request.user.id

        try:
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
        user_id = request.user.id

        try:
            question = QuestionSlider.objects.get(pk=post_data['question_id'])
            min_value, max_value = question.value_min, question.value_max

            answer_value = post_data['answer_value']

            if answer_value not in list(range(min_value, max_value + 1)):
                return HttpResponse(status=400, reason=f"Value {answer_value} is out of allowed range({min_value}-{max_value})")

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
        user_id = request.user.id

        try:

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

# QUESTIONS

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

    types = [QuestionSlider, QuestionLibre, QuestionChoixMultiple]
    serializers = [QuestionSliderSerializer, QuestionLibreSerializer, QuestionChoixMultipleSerializer]
    names = ['slider', 'libre', 'qcm']

    def get_tools(self, type):
        i = QuestionListByType.names.index(type)
        return QuestionListByType.types[i], QuestionListByType.serializers[i]

    def is_addable(self, questionnaire_id):
        questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
        # Check if the related Questionnaire is on
        return not questionnaire.MONTHSTART_START <= timezone.now() <= questionnaire.MONTHSTART_END and not questionnaire.MONTHEND_START <= timezone.now() <= questionnaire.MONTHEND_END

    def get(self, request, type, format=None):
        if type not in QuestionListByType.names:
            return HttpResponse(status=404)
        model, serializer = self.get_tools(type)
        questions = model.objects.all()
        serialize = serializer(questions, many=True)
        return JsonResponse(serialize.data, safe=False)

    def post(self, request, type, format=None):
        if type not in QuestionListByType.names:
            return HttpResponse(status=404)
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

    types = [QuestionSlider, QuestionLibre, QuestionChoixMultiple]
    serializers = [QuestionSliderSerializer, QuestionLibreSerializer, QuestionChoixMultipleSerializer]
    names = ['slider', 'libre', 'qcm']

    def get_object(self, type, pk):
        i = QuestionDetail.names.index(type)
        try:
            return QuestionDetail.types[i].objects.get(pk=pk), QuestionDetail.serializers[i]
        except QuestionDetail.types[i].DoesNotExist:
            return None

    def is_editable(self, fk_id):
        questionnaire = Questionnaire.objects.get(pk=2)
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
