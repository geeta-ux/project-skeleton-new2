from django.urls import path
from . import views

app_name = "psychometric"

urlpatterns = [
    # ENTRY POINT
    path('', views.entry_view, name='entry'),

    # Core flow
    path('screening/', views.screening_view, name='screening'),
    path('screening/process/', views.process_screening_view, name='process_screening'),
    path('hub/', views.hub_view, name='hub'),

    # Tests
    path('verbal/', views.verbal_view, name='verbal'),
    path('personality/', views.personality_view, name='personality'),
    path('sjt/', views.sjt_view, name='sjt'),

    # AI
    path('chat/', views.ai_chat_view, name='ai_chat'),
    path('generate-question/', views.generate_question_view, name='generate_question'),
    path('career-advice/', views.career_advice_view, name='career_advice'),

    # Legacy API fallbacks
    path('api/chat/', views.ai_chat_view),
    path('api/generate-question/', views.generate_question_view),
    path('api/career-advice/', views.career_advice_view),
]
