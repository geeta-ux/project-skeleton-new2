from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User  # your custom user model
        fields = ['email', 'name', 'password1', 'password2', 'gender', 'age_group', 'education', 'experience_level']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']
