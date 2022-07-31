from django.urls import path

from . import views

urlpatterns = [
    path('questionnaires/', views.questionnaires_list.as_view()),
    path('questionnaires/<int:pk>/', views.questionnaire_detail.as_view()),
    path('users/', views.user_list),
    path('users/<int:pk>/', views.user_detail),
    path('reponse/libre/', views.reponse_libre),
    path('reponse/slider/', views.reponse_slider),
    path('reponse/qcm/', views.reponse_qcm)
]