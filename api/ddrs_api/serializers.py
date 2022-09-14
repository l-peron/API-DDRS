import datetime
from django.forms import CharField
from rest_framework import serializers
from django.contrib.auth.models import User
from ddrs_api.models import QCMChamp, QuestionChoixMultiple, QuestionLibre, QuestionSlider, Questionnaire, RCMChamp, ReponseChoixMultiple, ReponseLibre, ReponseSlider

# Serializer for user
class UserSerializer(serializers.ModelSerializer):
        class Meta:
                model = User
                fields = ['id', 'username']

# Serializer for Question Slider
class QuestionSliderSerializer(serializers.ModelSerializer):
        class Meta:
                model = QuestionSlider
                fields = ['id', "title_text", "value_min", "value_max"]
        

# Serializer for QCMChamp
class QCMChampSerializer(serializers.ModelSerializer):
        class Meta:
                model = QCMChamp
                fields = ['id',"title_text", "question_id"]

# Serializer for Question Choix Multiple
class QuestionChoixMultipleSerializer(serializers.ModelSerializer):
        champs = serializers.SerializerMethodField()
        class Meta:
                model = QuestionChoixMultiple
                fields = ['id', "title_text", "champs"]
        # Used to retrieve referencing champs
        def get_champs(self, obj):
                champs = QCMChamp.objects.filter(question_id = obj)
                return QCMChampSerializer(champs, many = True).data

# Serializer for Question Libre
class QuestionLibreSerializer(serializers.ModelSerializer):
        class Meta:
                model = QuestionLibre
                fields = ['id', "title_text"]

# Serializer for Question Slider
class ReponseSliderSerializer(serializers.ModelSerializer):
        class Meta:
                model = ReponseSlider
                fields = '__all__'

# Serializer for QCMChamp
class RCMChampSerializer(serializers.ModelSerializer):
        class Meta:
                model = RCMChamp
                fields = "__all__"

# Serializer for Reponse Choix Multiple
class ReponseChoixMultipleSerializer(serializers.ModelSerializer):
        champs = serializers.SerializerMethodField()
        class Meta:
                model = ReponseChoixMultiple
                fields = "__all__"
        # Used to retrieve referencing champs
        def get_champs(self, obj):
                champs = RCMChamp.objects.filter(rcm_id = obj)
                return RCMChampSerializer(champs, many = True).data

# Serializer for Reponse Libre
class ReponseLibreSerializer(serializers.ModelSerializer):
        class Meta:
                model = ReponseLibre
                fields = "__all__"

# Serializer for Questionnaire
class QuestionnaireSerializer(serializers.ModelSerializer):
        questions = serializers.SerializerMethodField()
        class Meta:
                model = Questionnaire
                fields = "__all__"
        # Used to retrieve referencing questions
        def get_questions(self, obj):
                sliders = QuestionSlider.objects.filter(questionnaire_id=obj)
                choix_multiple = QuestionChoixMultiple.objects.filter(questionnaire_id=obj)
                libre = QuestionLibre.objects.filter(questionnaire_id=obj)
                return { 
                        "sliders" : QuestionSliderSerializer(sliders, many=True).data,
                        "choix_multiple" : QuestionChoixMultipleSerializer(choix_multiple, many=True).data,
                        "libre" : QuestionLibreSerializer(libre, many=True).data
                }

# QUESTIONS

# Serializer for Question Slider
class QuestionSliderSerializer(serializers.ModelSerializer):
        class Meta:
                model = QuestionSlider
                fields = ['id', "title_text", "value_min", "value_max", "questionnaire_id"]

# Serializer for Question Choix Multiple
class QuestionChoixMultipleSerializer(serializers.ModelSerializer):
        champs = serializers.SerializerMethodField()
        class Meta:
                model = QuestionChoixMultiple
                fields = ['id', "title_text", "champs", "questionnaire_id"]
        # Used to retrieve referencing champs
        def get_champs(self, obj):
                champs = QCMChamp.objects.filter(question_id = obj)
                return QCMChampSerializer(champs, many = True).data

# Serializer for Question Libre
class QuestionLibreSerializer(serializers.ModelSerializer):
        class Meta:
                model = QuestionLibre
                fields = ['id', "title_text", "questionnaire_id"]

