
from .models import Super
from .serializers import SuperSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SuperList(APIView):
    #Gets all Supers
    def get(self, request, format=None):
        super = Super.objects.all()
        serializer = SuperSerializer(super, many=True)
        return Response(serializer.data)
    
    #Creates Super
    def post(self, request, format=None):
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class SuperDetail(APIView):
    def print(self, request, format=None):
        pass
