from django.urls import path
import django_cas_ng.views
from . import views
from . import admin_views

urlpatterns = [
    path('users/', views.user_list.as_view()),
    path('users/<int:pk>/', views.user_detail.as_view()),
    path('accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('questionnaires/', views.questionnaires_list.as_view()),
    path('questionnaires/<int:pk>/', views.questionnaire_detail.as_view()),
    path('reponses/', views.reponse_list.as_view()),
    path('reponses/libre/', views.reponse_libre_list.as_view()),
    path('reponses/slider/', views.reponse_slider_list.as_view()),
    path('reponses/qcm/', views.reponse_qcm_list.as_view()),
    path('reponses/<str:type>/<int:pk>/', views.reponse_detail.as_view()),
    path('questions/', views.QuestionList.as_view()),
    path('questions/<str:type>/', views.QuestionListByType.as_view()),
    path('questions/<str:type>/<int:pk>/', views.QuestionDetail.as_view())
]