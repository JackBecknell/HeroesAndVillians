 
from .models import Super
from .serializers import SuperSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SuperList(APIView):
    #Gets all Supers
    def get(self, request, format=None):
        super_type = request.query_params.get('super_type')
        queryset = Super.objects.all()
        if super_type:
            queryset = queryset.filter(super_type__name=super_type)
        serializer = SuperSerializer(queryset, many=True)
        return Response(serializer.data)
    
    #Creates Super
    def post(self, request, format=None):
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class SuperDetail(APIView):
    def get_object(self, pk):
        try:
            return Super.objects.get(pk=pk)
        except Super.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        super = self.get_object(pk)
        serializer = SuperSerializer(super)
        return Response(serializer.data)

    #Updates single product by pk
    def put(self, request, pk, format=None):
        super = self.get_object(pk)
        serializer = SuperSerializer(super, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Deletes single Product by pk
    def delete(self, request, pk, format=None):
        super = self.get_object(pk)
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)