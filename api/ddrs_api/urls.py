from django.urls import path

from . import views

urlpatterns = [
    path('questionnaires/', views.questionnaires_list),
    path('questionnaires/<int:pk>/', views.questionnaire_detail),
    path('questions/', views.questions_list),
    path('questions/<int:pk>/', views.question_detail)
]
