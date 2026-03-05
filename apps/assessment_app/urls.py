from django.urls import path
from .views import (
    AssessmentIntroView, 
    AssessmentGeneratorView, 
    AssessmentTakeView, 
    AssessmentResultView,
    DownloadPlanPDFView
)

app_name = "assessment_app"

urlpatterns = [
    path('start/', AssessmentIntroView.as_view(), name='start'),
    path('generate/', AssessmentGeneratorView.as_view(), name='generate'),
    path('take/<int:pk>/', AssessmentTakeView.as_view(), name='take_test'),
    path('results/<int:pk>/', AssessmentResultView.as_view(), name='results'),
    path('results/<int:pk>/download/', DownloadPlanPDFView.as_view(), name='download_plan'),
]
