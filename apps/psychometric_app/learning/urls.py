from django.urls import path
from . import views

app_name = "psychometric"

urlpatterns = [
    path('', views.hub_view, name='hub'),
    path('verbal/', views.verbal_view, name='verbal'),
    path('personality/', views.personality_view, name='personality'),
    path('sjt/', views.sjt_view, name='sjt'),
    # AI Endpoints
    path('chat/', views.ai_chat_view, name='ai_chat'),
    path('generate-question/', views.generate_question_view, name='generate_question'),
    path('career-advice/', views.career_advice_view, name='career_advice'),
]
