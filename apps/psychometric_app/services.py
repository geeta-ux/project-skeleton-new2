from apps.careers_app.models import Career
from .models import PsychometricResponse
from apps.psychometric_app import models
from django.db.models import Avg



def calculate_psychometric_profile(user):
    from .models import PsychometricResponse
    from .services import map_profile_to_careers  # ensure import


    responses = PsychometricResponse.objects.filter(session__user=user)

    if not responses.exists():
        profile = {
            "personality_level": "-",
            "interest_type": "-",
            "value_orientation": "-",
            "recommended_careers": [],
        }
        return profile

    avg = responses.aggregate(avg_score=Avg("score"))["avg_score"]

    if avg <= 2:
        personality = "Reserved & Reflective"
    elif avg <= 4:
        personality = "Balanced & Adaptive"
    else:
        personality = "Expressive & Outgoing"

    profile = {
        "personality_level": personality,
        "interest_type": "Structured & Analytical",
        "value_orientation": "Stability & Security",
    }

    # Map to careers
    career_titles = map_profile_to_careers(profile)
    profile["recommended_careers"] = [
        {"title": c, "category": c, "description": ""} for c in career_titles
    ]

    return profile


# -----------------------
# SCORE → LABEL MAPPERS
# -----------------------

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


# -----------------------
# CAREER MAPPING
# -----------------------

def map_profile_to_careers(profile):
    """
    Takes psychometric profile and returns a list of recommended careers.
    """

    personality = profile.get("personality_level", "").lower()
    interest = profile.get("interest_type", "").lower()
    values = profile.get("value_orientation", "").lower()

    careers = set()

    # ---- Personality mapping ----
    if "reserved" in personality or "reflective" in personality:
        careers.update([
            "Data Analyst",
            "Research Assistant",
            "Software Developer",
            "Technical Writer"
        ])

    # ---- Interest mapping ----
    if "structured" in interest or "analytical" in interest:
        careers.update([
            "Accountant",
            "Statistician",
            "Quality Analyst",
            "Business Analyst",
        ])

    # ---- Values mapping ----
    if "stability" in values or "security" in values:
        careers.update([
            "Bank Officer",
            "Government Clerk",
            "Operations Coordinator",
            "Teacher"
        ])

    # Return sorted list for display
    return sorted(list(careers))

