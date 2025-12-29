# apps/psychometric_app/services.py

from .models import PsychometricSession

def calculate_psychometric_profile(user):
    session = PsychometricSession.objects.filter(
        user=user,
        completed_at__isnull=False
    ).latest('completed_at')

    responses = session.responses.select_related('question')

    scores = {
        'personality': 0,
        'interest': 0,
        'values': 0
    }

    for r in responses:
        if r.question.category in scores:
            scores[r.question.category] += r.score

    return {
        'personality_level': map_personality(scores['personality']),
        'interest_type': map_interest(scores['interest']),
        'value_orientation': map_values(scores['values']),
    }


def map_personality(score):
    if score < 30:
        return "Reserved & Reflective"
    elif score < 45:
        return "Balanced & Adaptive"
    return "Expressive & Outgoing"


def map_interest(score):
    if score < 30:
        return "Structured & Analytical"
    elif score < 45:
        return "Creative & Exploratory"
    return "People-Oriented & Leadership"


def map_values(score):
    if score < 30:
        return "Stability & Security"
    elif score < 45:
        return "Growth & Achievement"
    return "Purpose & Impact"
