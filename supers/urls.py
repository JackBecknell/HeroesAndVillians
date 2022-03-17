from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.SuperList.as_view()),
    path('<int:pk>/', views.SuperDetail.as_view())
]