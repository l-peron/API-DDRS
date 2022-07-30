from django.urls import path

from . import views
from . import admin_views

urlpatterns = [
    path('users/', views.user_list.as_view()),
    path('users/<int:pk>/', views.user_detail.as_view()),
    path('admin/', admin_views.admin_example.as_view()),
]