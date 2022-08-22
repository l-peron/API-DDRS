from django.urls import path
from django.contrib import admin
import django_cas_ng.views
from . import views

urlpatterns = [
    path('users/', views.user_list),
    path('users/<int:pk>/', views.user_detail),
    path('accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('questionnaires/', views.questionnaires_list.as_view()),
    path('questionnaires/<int:pk>/', views.questionnaire_detail.as_view()),
    path('reponse/libre/', views.reponse_libre),
    path('reponse/slider/', views.reponse_slider),
    path('reponse/qcm/', views.reponse_qcm),
    path('questions/', views.QuestionList.as_view()),
    path('questions/<str:type>/', views.QuestionListByType.as_view()),
    path('questions/<str:type>/<int:pk>/', views.QuestionDetail.as_view())
]