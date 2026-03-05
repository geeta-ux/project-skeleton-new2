from typing import Dict
from apps.assessment_app.models import CareerAssessment
from apps.careers_app.models import Career

# -----------------------------
# Normalize function
# -----------------------------
def normalize_answer(text: str) -> str:
    """
    Converts curly quotes to straight quotes, trims spaces,
    and forces lowercase to ensure consistent comparison.
    """
    if not text:
        return ""
    return (
        text.replace("’", "'")
            .replace("‘", "'")
            .replace("“", '"')
            .replace("”", '"')
            .strip()
            .lower()
    )

# -----------------------------
# Track → Career Profile mapping
# -----------------------------
TRACK_TO_PROFILE = {
    "analytical": ["Data Scientist", "Business Analyst", "AI Researcher"],
    "communication": ["Software Engineer", "Full-Stack Developer", "DevOps Engineer"],
    "creative": ["UI/UX Designer", "Product Designer"],
    "interpersonal": ["HR Specialist", "Customer Success Manager", "Career Coach"],
    "management": ["Project Manager", "Product Manager", "Operations Manager"]
}

# -----------------------------
# Career Skill Profiles
# -----------------------------
CAREER_SKILL_PROFILES = {
    "Data Scientist": {"python": 5, "statistics": 5, "machine_learning": 5, "data_visualization": 4, "communication": 3},
    "Business Analyst": {"excel": 5, "data_analysis": 5, "sql": 4, "critical_thinking": 4, "communication": 4},
    "AI Researcher": {"python": 5, "machine_learning": 5, "deep_learning": 5, "math": 5, "research": 4},
    "Software Engineer": {"programming": 5, "algorithms": 5, "system_design": 4, "databases": 4, "communication": 3},
    "HR Specialist": {"communication": 5, "empathy": 5, "conflict_resolution": 4, "organization": 4},
    # ... add others as needed
}

# -----------------------------
# Helpers
# -----------------------------
def choose_primary_secondary_tracks(per_track_scores: Dict[str, float]) -> tuple[str, str]:
    items = sorted(per_track_scores.items(), key=lambda x: x[1], reverse=True)
    primary = items[0][0] if items else "analytical"
    secondary = items[1][0] if len(items) > 1 else "communication"
    return primary, secondary

def recommend_careers(primary_track: str, limit=3):
    qs = Career.objects.filter(track__contains=[primary_track])
    if qs.exists():
        return list(qs[:limit])
    return list(Career.objects.all()[:limit])

def generate_five_year_plan_dynamic(per_track_scores: dict) -> list[dict]:
    # Simplified logic for now
    return [{"year": i+1, "goal": f"Goal for year {i+1}"} for i in range(5)]

def generate_gap_analysis(user_scores: dict, career_profile: dict) -> list[dict]:
    gap_table = []
    for skill, ideal_score in career_profile.items():
        user_score = float(user_scores.get(skill, 0))
        gap = ideal_score - user_score
        action = "No action needed" if gap <= 0 else f"Complete {gap} level(s) of learning in {skill}"
        gap_table.append({"skill": skill, "gap": max(gap, 0), "action": action})
    return gap_table

def generate_skill_gaps_from_result(result, career_name):
    # Wrapper for compatibility
    return {"gaps": []}


# -----------------------------
# Score Assessment (New Logic)
# -----------------------------
def score_assessment(assessment: CareerAssessment) -> dict:
    """
    Scores various sections based on the 'scores' JSON in CareerAssessment.
    Adapts the AI category names to the 'tracks' expected by Results app.
    """
    raw_scores = assessment.scores or {}
    
    # Map AI categories to Tracks/Sections
    # AI Categories: Logical Reasoning, Numerical Reasoning, Verbal Reasoning, Creative Thinking, Empathy
    
    section_scores = {
        "verbal": raw_scores.get("Verbal Reasoning", 0),
        "logical": raw_scores.get("Logical Reasoning", 0),
        "numerical": raw_scores.get("Numerical Reasoning", 0),
        "creative": raw_scores.get("Creative Thinking", 0),
        "empathy": raw_scores.get("Empathy", 0),
    }

    # Derived Tracks
    track_scores = {
        "analytical": section_scores["logical"] + section_scores["numerical"],
        "communication": section_scores["verbal"],
        "creative": section_scores["creative"],
        "interpersonal": section_scores["empathy"],
        # Management? maybe analytical + interpersonal
        "management": (section_scores["logical"] + section_scores["empathy"]) / 2
    }

    total_score = sum(section_scores.values())

    primary_track, secondary_track = choose_primary_secondary_tracks(track_scores)
    
    score_breakdown = {
        **section_scores,
        "tracks": track_scores,
        "total": total_score,
        "primary_track": primary_track,
        "secondary_track": secondary_track
    }

    return score_breakdown
