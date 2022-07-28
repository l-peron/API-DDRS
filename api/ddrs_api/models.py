from django.db import models
from django.contrib.auth.models import User

# 'Questionnaire' model
class Questionnaire(models.Model):
    # Title of the 'questionnaire'
    title_text = models.CharField(max_length=100)
    # Timespans
    # Starting span
    MONTHSTART_START = models.DateTimeField()
    MONTHSTART_END = models.DateTimeField()
    # End span
    MONTHEND_START = models.DateTimeField()
    MONTHEND_END = models.DateTimeField()

# Question model
class Question(models.Model):
    # Question
    title_text = models.CharField(max_length=300)
    # Linked 'questionnaire'
    # Many-to-one
    questionnaire_id = models.ForeignKey(Questionnaire, on_delete = models.CASCADE)

    class Meta:
        abstract = True

# Every type of questions :
# QuestionSlider model
class QuestionSlider(Question):
    value_min = models.IntegerField()
    value_max = models.IntegerField()

# QuestionChoixMultiple model
class QuestionChoixMultiple(Question):
    # No specific things
    # but is referenced by 'champs'
    pass

# QCMChamp model
class QCMChamp(models.Model):
    # Possible answer
    title_text = models.CharField(max_length = 100)
    # Linked 'Question'
    # Many-to-one
    question_id = models.ForeignKey(QuestionChoixMultiple, on_delete = models.CASCADE)

# QuestionLibre model
class QuestionLibre(Question):
    # No specific thing (only uses the title)
    pass

# 'Reponse' model
class Reponse(models.Model):
    # Posted date
    answer_date = models.DateTimeField(null=True, blank=True)
    # Linked 'User'
    # Many-to-one
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)

    # Declared as an abstract model
    class Meta:
        abstract = True

# Every type of responses :
# ReponseSlider model
class ReponseSlider(Reponse):
    # Answer's value
    answer_value = models.IntegerField()

    # Linked 'Question'
    # One-to-one
    question_id = models.OneToOneField(QuestionSlider, on_delete = models.CASCADE)

# ReponseChoixMultiple model
class ReponseChoixMultiple(Reponse):
    # Linked 'Question'
    # One-to-one
    question_id = models.OneToOneField(QuestionChoixMultiple, on_delete = models.CASCADE)

# RCMChamp model
class RCMChamp(models.Model):
    checked_boolean = models.BooleanField(default=False)
    # Linked 'ReponseChoixMultiple'
    # Many-to-one
    rcm_id = models.ForeignKey(ReponseChoixMultiple, on_delete = models.CASCADE)
    # Linked 'QCMChamp'
    # One-to-one
    qcmchamp_id = models.OneToOneField(QCMChamp, on_delete = models.CASCADE)

# ReponseLibre model
class ReponseLibre(Reponse):
    # Input text answer
    answer_text = models.CharField(max_length=300)
    # Linked 'Question'
    # One-to-one
    question_id = models.OneToOneField(QuestionLibre, on_delete = models.CASCADE)
