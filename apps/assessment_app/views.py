from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from rest_framework import viewsets, permissions
from apps.assessment_app.services import (
    score_assessment,
    choose_primary_secondary_tracks,
    recommend_careers
)
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from apps.results_app.models import Result
from .models import Question, Assessment, Response
from .serializers import QuestionSerializer, AssessmentSerializer, ResponseSerializer


# -----------------------------
# DRF ViewSets
# -----------------------------
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
# WEB ASSESSMENT VIEW
# -----------------------------
@method_decorator(csrf_protect, name="dispatch")
class AssessmentQuestionView(View):
    template_name = "assessment/question.html"

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        # Ensure assessment exists
        assessment, _ = Assessment.objects.get_or_create(
            user=request.user,
            completed_at=None
        )

        return render(request, self.template_name, {
            "question": question,
            "section": question.section,
        })

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        selected_option_index = int(request.POST.get("answer", 0)) - 1
        selected_answer = question.options[selected_option_index]

        score = question.weight if selected_answer == question.correct_answer else 0

        # Get existing assessment
        assessment, _ = Assessment.objects.get_or_create(
            user=request.user,
            completed_at=None
        )

        # Save response
        Response.objects.create(
            user=request.user,
            assessment=assessment,
            question=question,
            answer=selected_answer,
            score=score,
        )

        # Get next question
        next_question = Question.objects.filter(pk__gt=pk).order_by("pk").first()

        if next_question:
            return redirect("assessment_app:question", pk=next_question.pk)

        # LAST QUESTION → Score assessment
        score_data = score_assessment(assessment)
        primary, secondary = choose_primary_secondary_tracks(score_data["tracks"])

        Result.objects.update_or_create(
            user=request.user,
            defaults={
                "score_breakdown": score_data,
                "primary_track": primary,
                "secondary_track": secondary,
                "scores": score_data["tracks"],
                "careers": recommend_careers(primary),
            }
        )

        assessment.completed_at = timezone.now()
        assessment.save()

        return redirect("results_app:latest_summary")


# -----------------------------
# Start Assessment
# -----------------------------
class AssessmentStartView(View):
    def get(self, request, *args, **kwargs):
        first_question = Question.objects.order_by("pk").first()
        if first_question:
            return redirect("assessment_app:question", pk=first_question.pk)
        return redirect('base')
