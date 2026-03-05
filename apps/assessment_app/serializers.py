from rest_framework import serializers
from .models import CareerAssessment

class CareerAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerAssessment
        fields = '__all__'
