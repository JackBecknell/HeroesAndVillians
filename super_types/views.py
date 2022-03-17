from .serializers import SuperTypeSerializer
from .models import SuperType
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SuperTypeList(APIView):
    def get(self, request, format=None):
        queryset = SuperType.objects.all()
        serializer = SuperTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SuperTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class SuperTypeDetail(APIView):
    def get_object(self, pk):
        try:
            return SuperType.objects.get(pk=pk)
        except SuperType.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        super_type = self.get_object(pk)
        serializer = SuperTypeSerializer(super_type)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        super_type = self.get_object(pk)
        serializer = SuperTypeSerializer(super_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        super_type = self.get_object(pk)
        super_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)