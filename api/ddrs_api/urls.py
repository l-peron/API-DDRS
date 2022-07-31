from django.urls import path

from . import views

urlpatterns = [
    path('questionnaires/', views.questionnaires_list.as_view()),
    path('questionnaires/<int:pk>/', views.questionnaire_detail.as_view()),
]