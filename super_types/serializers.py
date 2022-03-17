from rest_framework import serializers
from .models import SuperTypes

class SuperTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperTypes
        fields = ['id', 'name']