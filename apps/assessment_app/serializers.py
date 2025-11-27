from rest_framework import serializers
from .models import Question, Assessment, Response

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'

class AssessmentSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True, read_only=True)
    class Meta:
        model = Assessment
        fields = '__all__'
