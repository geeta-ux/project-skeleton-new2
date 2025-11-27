from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AssessmentViewSet, ResponseViewSet
from .views import AssessmentStartView, AssessmentQuestionView

app_name = "assessment_app"

router = DefaultRouter()
router.register(r"questions", QuestionViewSet)
router.register(r"assessments", AssessmentViewSet)
router.register(r"responses", ResponseViewSet)

urlpatterns = [
    path("start/", AssessmentStartView.as_view(), name="start"),  # web page
    path("take/question/<int:pk>/", AssessmentQuestionView.as_view(), name="question"),
]
