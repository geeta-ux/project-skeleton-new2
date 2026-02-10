from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
import json

from .models import Topic, ScreeningQuestion, ScreeningSession, ScreeningResponse
from .ai_service import AIService


@login_required
def entry_view(request):
    session = ScreeningSession.objects.filter(user=request.user).first()
    if not session or not session.is_completed:
        return redirect("psychometric:screening")
    return redirect("psychometric:hub")


@login_required
def hub_view(request):
    if not getattr(request.user, 'has_psychometric_access', False):
        messages.warning(
            request,
            "Your account is pending psychometric access approval by an administrator."
        )
        return redirect('base')

    recent_session = ScreeningSession.objects.filter(
        user=request.user,
        is_completed=True,
        timestamp__gte=timezone.now() - timezone.timedelta(days=30)
    ).first()

    if not recent_session:
        return redirect('psychometric:screening')

    test_type = request.GET.get('test_type')
    topics = Topic.objects.all()

    return render(request, 'learning/hub.html', {
        'topics': topics,
        'highlighted_test': test_type,
        'session': recent_session
    })


@login_required
def screening_view(request):
    # Optional: check user access
    if not getattr(request.user, 'has_psychometric_access', False):
        messages.warning(request, "Your account is pending psychometric access approval.")
        return redirect('base')

    # Get all active questions, ordered
    questions = ScreeningQuestion.objects.filter(is_active=True).order_by('order')

    if not questions.exists():
        messages.warning(request, "No screening questions available. Contact admin.")
        return redirect('base')

    return render(request, "learning/screening.html", {"questions": questions})

@login_required
def process_screening_view(request):
    if request.method != 'POST':
        return redirect('psychometric:screening')
    
    if not getattr(request.user, 'has_psychometric_access', False):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    session = ScreeningSession.objects.create(user=request.user)
    score_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    questions = ScreeningQuestion.objects.all()
    domain_totals = {}

    for q in questions:
        choice = request.POST.get(f'question_{q.id}')
        if choice:
            score = score_map.get(choice, 0)
            ScreeningResponse.objects.create(
                session=session,
                question=q,
                selected_choice=choice,
                score=score
            )
            domain_name = q.domain.name
            domain_totals[domain_name] = domain_totals.get(domain_name, 0) + score

    session.domain_scores = domain_totals

    # Risk assessment
    moderate_domains = [d for d, s in domain_totals.items() if s >= 4]
    high_domains = [d for d, s in domain_totals.items() if s >= 6]
    duration_long = domain_totals.get('Duration', 0) >= 2 
    functional_impact = domain_totals.get('Functional Capacity', 0) >= 4 

    risk_level = 'low'
    recommendation = "Your responses suggest you are in a stable state to begin psychometric testing."
    route_to = 'hub'

    if len(high_domains) >= 3 or (len(high_domains) >= 1 and duration_long and functional_impact):
        risk_level = 'high'
        recommendation = "Your responses suggest patterns that may benefit from professional evaluation."
        route_to = 'exit'
    elif len(moderate_domains) >= 2 and duration_long and functional_impact:
        risk_level = 'medium'
        recommendation = "Some indicators of stress detected. You may proceed with caution."
        route_to = 'hub'

    # Routing logic if not high risk
    if risk_level != 'high':
        cognition_score = domain_totals.get('Cognition', 0)
        mood_reg_score = domain_totals.get('Mood', 0) + domain_totals.get('Emotional Regulation', 0)
        anxiety_social_score = domain_totals.get('Anxiety', 0) + domain_totals.get('Social Functioning', 0)

        if mood_reg_score >= 4:
            route_to = 'personality'
        elif anxiety_social_score >= 4:
            route_to = 'sjt'
        elif cognition_score <= 1:
            route_to = 'verbal'
        else:
            route_to = 'hub'

    session.risk_level = risk_level
    session.recommendation = recommendation
    session.is_completed = True
    session.save()

    return render(request, 'learning/screening_result.html', {
        'session': session,
        'route_to': route_to,
        'moderate_domains': moderate_domains,
        'high_domains': high_domains
    })


def get_topic_content(slug):
    topic = get_object_or_404(Topic, slug=slug)
    contents = topic.contents.all()
    return {'topic': topic, 'contents': contents}


def verbal_view(request):
    return render(request, 'learning/verbal.html', get_topic_content('verbal'))


def personality_view(request):
    return render(request, 'learning/personality.html', get_topic_content('personality'))


def sjt_view(request):
    return render(request, 'learning/sjt.html', get_topic_content('sjt'))


@csrf_exempt
def ai_chat_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        topic_slug = data.get('topic', 'general')
        response = AIService.get_chat_response(topic_slug, message)
        return JsonResponse({'response': response})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def generate_question_view(request):
    topic_slug = request.GET.get('topic')
    if not topic_slug:
        return JsonResponse({'error': 'Missing topic'}, status=400)

    questions = AIService.generate_question(topic_slug)
    if questions:
        return JsonResponse({'questions': questions})
    return JsonResponse({'error': 'Could not generate questions'}, status=500)


@csrf_exempt
def career_advice_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        topic = data.get('topic')
        user_data = data.get('performance_data')
        recommendations = AIService.get_career_advice(topic, user_data)
        return JsonResponse({'careers': recommendations})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
