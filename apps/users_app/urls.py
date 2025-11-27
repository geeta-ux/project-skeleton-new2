from django.urls import path
from .views import SignUpView, LoginView
from .views import LogoutGetView


app_name = "users_app"

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutGetView.as_view(), name="logout"),
]
