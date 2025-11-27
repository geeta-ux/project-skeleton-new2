from rest_framework import serializers
from .models import Career, CareerKB

class CareerKBSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerKB
        fields = '__all__'

class CareerSerializer(serializers.ModelSerializer):
    kb_entries = CareerKBSerializer(many=True, read_only=True)
    class Meta:
        model = Career
        fields = '__all__'
