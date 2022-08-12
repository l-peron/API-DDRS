from django.urls import path

from . import views

urlpatterns = [
    path('questionnaires/', views.questionnaires_list.as_view()),
    path('questionnaires/<int:pk>/', views.questionnaire_detail.as_view()),
    path('users/<int:pk>/', views.user_detail),
    path('reponses/', views.reponse_list.as_view()),
    path('reponses/libre/', views.reponse_libre_list.as_view()),
    path('reponses/slider/', views.reponse_slider_list.as_view()),
    path('reponses/qcm/', views.reponse_qcm_list.as_view())
]