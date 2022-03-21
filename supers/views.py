 
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
    def get(self, request, format=None):
        #checks query params for name1 and name2
        super_one_name = request.query_params.get('name1')
        super_two_name = request.query_params.get('name2')
        #if statment checks to see if either variable holds a value, if they do than this indicates the user wants to compare powers for two supers.
        if super_one_name and super_two_name:
            #Both vars below search through Super objects by using the query parameter which should be a valid name in the database for Super.
            super_one = Super.objects.get(name=super_one_name)
            super_two = Super.objects.get(name=super_two_name)
            #Both vars below create a serializer for each Super in order to eventually be passed back.
            serializer_one = SuperSerializer(super_one)
            serializer_two = SuperSerializer(super_two)
            custom_response_dict = {}
            #if and elif statment look into both supers and count the number of powers they possess
            #depending on who has more of less determines a winner, loser, or a tie by utilizing a dictionary.
            if (super_one.powers.count()) > (super_two.powers.count()):
                custom_response_dict['WINNER then LOSER'] = {
                    "Winner": serializer_one.data,
                    "Loser" : serializer_two.data,
                    }
                return Response(custom_response_dict)
            elif (super_two.powers.count()) > (super_one.powers.count()):
                custom_response_dict['WINNER and LOSER'] = {
                    "Winner": serializer_two.data,
                    "Loser" : serializer_one.data,
                    }
                return Response(custom_response_dict)
            else:
                custom_response_dict['A TIE'] = {
                    "First Super": serializer_one.data,
                    "Second Super": serializer_two.data
                }
                return Response(custom_response_dict)
        #var looks to see if there was a query param called 'super_type' if there was it will contain the value of what
        #the user passed in the query.
        super_type = request.query_params.get('super_type')
        all_supers = Super.objects.all()
        #if super_type was a param passed and if it is equal to Hero or Villian then we return all heroes or villians depending
        #upon what the query specified
        if super_type == 'Hero' or super_type == 'Villain':
            queryset = all_supers.filter(super_type__name=super_type)
            serializer = SuperSerializer(queryset, many=True)  
            return Response(serializer.data) 
        #if super_type wasn't set to anything a custom table of both heroes and villains are returned.        
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
            serializer = SuperSerializer(all_supers, many=True)
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


#Class super patch is dedicated to adding a power to a hero who hadn't previously had it before.
class SuperPatch(APIView):
    def get_super(self, pk):
        try:
            return Super.objects.get(pk=pk)
        except Super.DoesNotExist:
            raise Http404

    def get_power(self, pk):
        try:
            return Power.objects.get(pk=pk)
        except Power.DoesNotExist:
            raise Http404

    #Calls get_object and returns 'Super' to allow a power to be added
    def patch(self, request, pk, fk, format=None):
        power_to_add = self.get_power(fk)
        super = self.get_super(pk)
        super.powers.add(power_to_add)
        serializer = SuperSerializer(super)
        return Response(serializer.data)


        