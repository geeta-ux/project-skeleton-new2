# apps/psychometric_app/views.py

from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import PsychometricSession, PsychometricQuestion, PsychometricResponse

from .services import map_profile_to_careers

from .services import calculate_psychometric_profile
from .pdf_utils import generate_psychometric_pdf


@login_required
def start_psychometric(request):
    # Create new session
    session = PsychometricSession.objects.create(
        user=request.user,
        session_type="standalone",
        started_at=timezone.now()
    )

    return redirect("psychometric_app:questions", session_id=session.id)



@login_required
def psychometric_report(request):
    profile = calculate_psychometric_profile(request.user)
    return render(request, 'psychometric/report.html', {
        'profile': profile
    })
LIKERT_CHOICES = [
    (1, "Strongly Disagree"),
    (2, "Disagree"),
    (3, "Neutral"),
    (4, "Agree"),
    (5, "Strongly Agree"),
]

@login_required
def answer_questions(request, session_id):
    session = get_object_or_404(PsychometricSession, id=session_id, user=request.user)
    questions = PsychometricQuestion.objects.filter(is_active=True)

    if request.method == "POST":
        for q in questions:
            score = request.POST.get(f"q_{q.id}")
            if score:
                PsychometricResponse.objects.update_or_create(
                    session=session,
                    question=q,
                    defaults={"score": int(score)}
                )

        # Mark session as completed
        session.completed_at = timezone.now()
        session.save()

        return redirect('psychometric_app:report')

    return render(request, 'psychometric/questions.html', {
        'session': session,
        'questions': questions,
        'likert_choices': LIKERT_CHOICES
    })

@login_required
def psychometric_report(request):
    profile = calculate_psychometric_profile(request.user)

    recommended_careers = map_profile_to_careers(profile)

    return render(request, 'psychometric/report.html', {
        'profile': profile,
        'recommended_careers': recommended_careers
    })



@login_required
def download_psychometric_pdf(request):
    profile = calculate_psychometric_profile(request.user)

    # add careers
    profile["recommended_careers"] = map_profile_to_careers(profile)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=\"psychometric_report.pdf\"'

    generate_psychometric_pdf(response, profile)
    return response



