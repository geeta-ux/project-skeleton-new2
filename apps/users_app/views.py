from django.http import HttpResponseRedirect
from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer

from django.views.generic import CreateView, FormView, View
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout



# -----------------------------
# DRF ViewSet
# -----------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# -----------------------------
# Sign-Up View
# -----------------------------
class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'auth/sign-up.html'
    success_url = reverse_lazy('users_app:login')  # adjust to your login URL

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

# -----------------------------
# Login View
# -----------------------------
class LoginView(FormView):
    form_class = AuthenticationForm  # default Django auth form
    template_name = 'auth/login.html'
    success_url = reverse_lazy('base')  # adjust to your homepage

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)
    
class LogoutGetView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('base'))

