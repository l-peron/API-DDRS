from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from ddrs_api.serializers import QuestionnaireSerializer, QuestionChoixMultipleSerializer, QuestionSliderSerializer, \
    QuestionLibreSerializer, QCMChampSerializer, UserSerializer
from ddrs_api.models import Questionnaire, Question
from ddrs_api.models import QuestionSlider, QuestionChoixMultiple, QuestionLibre
from ddrs_api.models import ReponseSlider, ReponseChoixMultiple, ReponseLibre
from ddrs_api.models import User, RCMChamp, QCMChamp


@csrf_exempt
def user_list(request):
    """
    List all Users
    """
    if request.method == 'GET':
        utilisateurs = User.objects.all()
        serializer = UserSerializer(utilisateurs, many=True)
        return JsonResponse(serializer.data, safe=False)

    # Error if not GET
    return HttpResponse(status=400)


@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve data about a specific Utilisateur
    """
    try:
        utilisateur = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(utilisateur)
        return JsonResponse(serializer.data)

    # Error if not GET
    return HttpResponse(status=400)

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
        """
        post_data = request.data

        try:
            serializer = QuestionnaireSerializer(data=post_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return HttpResponse(status=400)
        except KeyError:
            # 400 Bad Request
            return HttpResponse(status=400)


class questionnaire_detail(APIView):
    def get(self, request, *args, **kwargs):
        """
        Retrieve data about a specific Questionnaire
        """
        try:
            questionnaire = Questionnaire.objects.get(pk=kwargs['pk'])
        except Questionnaire.DoesNotExist:
            return HttpResponse(status=404)

        serializer = QuestionnaireSerializer(questionnaire)
        return JsonResponse(serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Delete a specific Questionnaire
        """
        try:
            questionnaire = Questionnaire.objects.get(pk=kwargs['pk'])
        except Questionnaire.DoesNotExist:
            return HttpResponse(status=404)

        questionnaire.delete()
        return HttpResponse(status=200)


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
            existing_entry = ReponseLibre.objects.get(question=question_id)  # user=user
            if existing_entry:
                existing_entry.answer_text = answer_text
                existing_entry.save()
                # Not sure if the user should be redirected or if it should just return a flag to indicate whether or
                # not the query was successful
                return HttpResponse(status=201)
        except ReponseLibre.DoesNotExist:
            question = QuestionLibre.objects.get(pk=question_id)
            new_entry = ReponseLibre(answer_date=datetime.now(), answer_text=answer_text, question=question)
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
            return HttpResponse(status=400,
                                reason=f"Value {answer_value} is out of allowed range({min_value}-{max_value})")

        try:
            existing_entry = ReponseSlider.objects.get(question=question_id)  # user=user
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
        existing_answer = ReponseChoixMultiple.objects.get(question=question_id)  # user=user
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
