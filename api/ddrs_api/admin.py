from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(QuestionSlider)
admin.site.register(QuestionChoixMultiple)
admin.site.register(QCMChamp)
admin.site.register(QuestionLibre)
admin.site.register(Reponse)
admin.site.register(ReponseSlider)
admin.site.register(ReponseChoixMultiple)
admin.site.register(RCMChamp)
admin.site.register(ReponseLibre)