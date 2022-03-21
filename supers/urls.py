from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .models import Super

urlpatterns = [
    path('', views.SuperList.as_view()),
    path('<int:pk>/', views.SuperDetail.as_view()),
    path('<int:pk>/<int:fk>/', views.SuperPatch.as_view()),
]