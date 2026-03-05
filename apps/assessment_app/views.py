from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
import json

from .models import CareerAssessment
from .ai_utils import AICareerService

class AssessmentIntroView(LoginRequiredMixin, View):
    """
    Checks if user has necessary profile details.
    Displays instructions.
    """
    template_name = "assessment/intro.html"

    def get(self, request):
        user = request.user
        missing_fields = []
        if not user.age_group: missing_fields.append("Age Group")
        if not user.education: missing_fields.append("Education")
        
        # Experience is optional/conditional, but good to check if we rely on it
        # but let's just warn about core demographics
        
        if missing_fields:
            messages.warning(request, f"Please update your profile: {', '.join(missing_fields)}")
            # You might want to redirect to a profile edit page here
            # return redirect('users_app:profile_edit') 
            # For now, just show the intro but maybe disable start?
            
        return render(request, self.template_name, {"missing_fields": missing_fields})

class AssessmentGeneratorView(LoginRequiredMixin, View):
    """
    Generates questions via AI and creates a new Assessment session.
    Redirects to the taking page.
    """
    def post(self, request):
        user = request.user
        
        # Prepare profile for AI
        profile = {
            "age_group": user.age_group,
            "education": user.education,
            "experience_level": user.experience_level,
            "gender": user.gender
        }
        
        # Generate questions
        questions = AICareerService.generate_questions(profile)
        
        if not questions:
            messages.error(request, "Failed to generate assessment. Please try again.")
            return redirect("assessment_app:start")
            
        # Create Assessment record
        assessment = CareerAssessment.objects.create(
            user=user,
            questions_data=questions,
            answers_data={},
            scores={}
        )
        
        return redirect("assessment_app:take_test", pk=assessment.id)

class AssessmentTakeView(LoginRequiredMixin, View):
    """
    Renders the test page with the generated questions.
    """
    template_name = "assessment/test.html"

    def get(self, request, pk):
        assessment = get_object_or_404(CareerAssessment, pk=pk, user=request.user)
        
        if assessment.completed:
            return redirect("assessment_app:results", pk=assessment.id)
            
        return render(request, self.template_name, {
            "assessment": assessment,
            "questions": assessment.questions_data
        })

    def post(self, request, pk):
        assessment = get_object_or_404(CareerAssessment, pk=pk, user=request.user)
        
        # Collect answers
        answers = {}
        for key, value in request.POST.items():
            if key.startswith("question_"):
                q_id = key.split("_")[1]
                answers[q_id] = value
        
        assessment.answers_data = answers
        
        # Calculate scores
        scores = AICareerService.calculate_scores(assessment.questions_data, answers)
        assessment.scores = scores
        
        # Generate Insights
        profile = {
            "age_group": request.user.age_group,
            "education": request.user.education,
            "experience_level": request.user.experience_level
        }
        assessment.insights = AICareerService.generate_career_insights(scores, profile)
        
        assessment.completed = True
        assessment.save()
        
        return redirect("assessment_app:results", pk=assessment.id)

class AssessmentResultView(LoginRequiredMixin, View):
    """
    Displays the results with charts and insights.
    """
    template_name = "assessment/results.html"

    def get(self, request, pk):
        assessment = get_object_or_404(CareerAssessment, pk=pk, user=request.user)
        
        if not assessment.completed:
            return redirect("assessment_app:take_test", pk=assessment.id)
            
        # PROACTIVE FIX: If Numerical score is 0 but answers exist, re-calculate
        # This fixes old results that failed due to the previous strict scoring logic.
        numerical_score = assessment.scores.get("numerical", 0)
        logical_score = assessment.scores.get("logical", 0)
        
        if (numerical_score == 0 or logical_score == 0) and assessment.answers_data:
            print(f"DEBUG: Proactively re-calculating scores for Assessment {assessment.id}")
            new_scores = AICareerService.calculate_scores(assessment.questions_data, assessment.answers_data)
            assessment.scores = new_scores
            
            # Also regenerate insights with the corrected scores
            profile = {
                "age_group": getattr(request.user, 'age_group', 'unknown'),
                "education": getattr(request.user, 'education', 'unknown'),
                "experience_level": getattr(request.user, 'experience_level', 'unknown')
            }
            assessment.insights = AICareerService.generate_career_insights(new_scores, profile)
            assessment.save()

        # Prepare score list for easier template rendering
        score_details = []
        for key, label in AICareerService.CATEGORIES.items():
            score_details.append({
                "label": label,
                "score": assessment.scores.get(key, 0)
            })

        # Prepare radar chart labels and data
        chart_data = [
            assessment.scores.get("logical", 0),
            assessment.scores.get("numerical", 0),
            assessment.scores.get("verbal", 0),
            assessment.scores.get("creative", 0),
            assessment.scores.get("empathy", 0)
        ]

        return render(request, self.template_name, {
            "assessment": assessment,
            "score_details": score_details,
            "total_score": assessment.scores.get("total", 0),
            "primary_track": AICareerService.CATEGORIES.get(assessment.scores.get("primary_track"), "General"),
            "secondary_track": AICareerService.CATEGORIES.get(assessment.scores.get("secondary_track"), "General"),
            "chart_data": json.dumps(chart_data),
            "insights": assessment.insights
        })

class DownloadPlanPDFView(LoginRequiredMixin, View):
    """
    View to download the career plan as a PDF.
    """
    def get(self, request, pk):
        assessment = get_object_or_404(CareerAssessment, pk=pk, user=request.user)
        
        # For now, return HTML for PDF rendering
        # If xhtml2pdf is not installed, we can just return a clean HTML page
        context = {
            "user": request.user,
            "result": assessment,
            "primary_track": AICareerService.CATEGORIES.get(assessment.scores.get("primary_track"), "General"),
            "secondary_track": AICareerService.CATEGORIES.get(assessment.scores.get("secondary_track"), "General"),
            "plans": assessment.insights.get('roadmap', [])
        }
        return render(request, "results/plan_pdf.html", context)