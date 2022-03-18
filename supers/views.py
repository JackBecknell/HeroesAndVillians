 
from unicodedata import name
from .models import Super
from powers.models import Power
from .serializers import SuperSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from super_types.models import SuperType

class SuperList(APIView):
    #Gets all Supers and can also filter for heroes or villians based off of the postman query.
    def get(self, request, format=None):
        super_type = request.query_params.get('super_type')
        queryset = Super.objects.all()
        all_supers = Super.objects.all()
        if super_type == 'Hero' or super_type == 'Villain':
            queryset = all_supers.filter(super_type__name=super_type)
            serializer = SuperSerializer(queryset, many=True)  
            return Response(serializer.data)         
        elif super_type == '':
            queryset = {}
            types = SuperType.objects.all()
            for type in types:
                supers = Super.objects.filter(super_type_id=type.id)
                super_serializer = SuperSerializer(supers, many=True)
                queryset[type.name] = {
                    "supers": super_serializer.data
                }
            return Response(queryset)
        else:
            queryset = Super.objects.all()
            serializer = SuperSerializer(queryset, many=True)
            return Response(serializer.data)

    #Creates Super
    def post(self, request, format=None):
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class SuperDetail(APIView):
    #Gets object by pk
    def get_object(self, pk):
        try:
            return Super.objects.get(pk=pk)
        except Super.DoesNotExist:
            raise Http404
    #Calls get_object and returns serialized object
    def get(self, request, pk, format=None):
        super = self.get_object(pk)
        serializer = SuperSerializer(super)
        return Response(serializer.data)

    #Calls get_object and updates single super
    def put(self, request, pk, format=None):
        super = self.get_object(pk)
        serializer = SuperSerializer(super, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Calls get_object and deletes single super
    def delete(self, request, pk, format=None):
        super = self.get_object(pk)
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SuperPatch(APIView):
    def get_object(self, pk):
        try:
            return Super.objects.get(pk=pk)
        except Super.DoesNotExist:
            raise Http404
    #Calls get_object and returns 'Super' to allow a power to be added
    def patch(self, request, pk, fk, format=None):
        power_to_add = Power.objects.get(pk=fk)
        super = self.get_object(pk)
        super.powers.add(power_to_add)
        serializer = SuperSerializer(super)
        return Response(serializer.data)

    
















def query_by_type(self, query_super_type):
        all_supers = Super.objects.all()
        if query_super_type == 'Hero' or query_super_type == 'Villian':
            queryset = all_supers.filter(super_type__name=query_super_type)
            serializer = SuperSerializer(queryset, many=True)  
            return Response(serializer.data)      
        else:
            queryset = {}
            types = SuperType.objects.all()
            for type in types:
                supers = Super.objects.filter(super_type_id=type.id)
                serializer = SuperSerializer(supers, many=True)
                queryset[type.name] = {
                    "supers": serializer.data
                }
            return Response(serializer.data)