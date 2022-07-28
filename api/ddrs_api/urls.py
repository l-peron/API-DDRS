from django.urls import path

from . import views

urlpatterns = [
    path('questionnaires/', views.questionnaires_list),
    path('questionnaires/<int:pk>/', views.questionnaire_detail),
    path('questions/', views.QuestionList.as_view()),
    path('questions/<str:type>/', views.QuestionListByType.as_view()),
    path('questions/<str:type>/<int:pk>/', views.QuestionDetail.as_view())
]
