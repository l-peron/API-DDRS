from django.urls import path
from django.contrib import admin
import django_cas_ng.views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('questionnaires/', views.questionnaires_list),
    path('questionnaires/<int:pk>/', views.questionnaire_detail),
    path('questions/', views.QuestionList.as_view()),
    path('questions/<str:type>/', views.QuestionListByType.as_view()),
    path('questions/<str:type>/<int:pk>/', views.QuestionDetail.as_view())
]
