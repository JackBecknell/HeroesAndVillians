from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.SuperTypeList.as_view()),
    path('<int:pk>/', views.SuperTypeDetail.as_view())
]