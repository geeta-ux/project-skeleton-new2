from django.urls import path
from . import views

app_name = 'psychometric_app'   # 🔥 IMPORTANT: match template namespace

urlpatterns = [
    path('start/', views.start_psychometric, name='start'),
    path('questions/<int:session_id>/', views.answer_questions, name='questions'),
    path('report/', views.psychometric_report, name='report'),
    path('download-pdf/', views.download_psychometric_pdf, name='download_pdf'),
]

