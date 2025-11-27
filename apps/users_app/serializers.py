from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'name', 
            'email', 
            'is_admin',
            'is_staff',
            'is_superuser',
            'is_active',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'created_at'
        ]
