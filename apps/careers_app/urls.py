from django.urls import path
from .views import careers_list, career_detail, career_kb_detail

app_name = "careers_app"

urlpatterns = [
    path("", careers_list, name="list"),
    path("<int:pk>/", career_detail, name="detail"),
    path("kb/<int:pk>/", career_kb_detail, name="kb_detail"),
]
