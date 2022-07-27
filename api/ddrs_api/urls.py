from django.urls import path

from . import views

urlpatterns = [
    path('questionnaires/', views.questionnaires_list),
    path('questionnaires/<int:pk>/', views.questionnaire_detail)
]