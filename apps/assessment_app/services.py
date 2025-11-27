# apps/assessment_app/services.py
from typing import Dict
from unicodedata import normalize
from apps.assessment_app.models import Assessment, Response, Question
from apps.results_app.models import Result
from apps.careers_app.models import Career

# -----------------------------
# Normalize function (IMPORTANT)
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
    "analytical": "Data Science",
    "communication": "General",
    "creative": "Design",
    "interpersonal": "General",
}

# -----------------------------
# Career Skill Profiles
# -----------------------------
CAREER_SKILL_PROFILES = {
    "Data Science": {
        "Python": 5,
        "Statistics": 5,
        "ML/AI": 5,
        "Data Visualization": 4,
        "Communication": 3
    },
    "Software Engineering": {
        "Python": 5,
        "Algorithms": 5,
        "System Design": 4,
        "Databases": 4,
        "Communication": 3
    },
    "Logical": {
        "Problem Solving": 5,
        "Reasoning": 5,
        "Debugging": 4,
        "Algorithms": 3
    },
    "General": {
        "Fundamentals": 5,
        "Projects": 4,
        "Professional Skills": 3
    }
}

# -----------------------------
# Generate Skill Gaps
# -----------------------------
def generate_gap_analysis(user_scores: dict, career_profile: dict) -> list[dict]:
    gap_table = []
    for skill, ideal_score in career_profile.items():
        user_score = float(user_scores.get(skill, 0))
        gap = ideal_score - user_score
        action = (
            "No action needed" if gap <= 0
            else f"Complete {gap} level(s) of learning in {skill}"
        )
        gap_table.append({
            "skill": skill,
            "gap": max(gap, 0),
            "action": action
        })
    return gap_table

# Wrapper for old usage
def generate_skill_gaps_from_result(result):
    user_scores = result.scores or {}
    mapped_profile = TRACK_TO_PROFILE.get(result.primary_track, "General")
    career_profile = CAREER_SKILL_PROFILES.get(mapped_profile, {})

    gaps = generate_gap_analysis(user_scores, career_profile)

    return {"gaps": gaps}

# -----------------------------
# Score Assessment
# -----------------------------
def score_assessment(assessment: Assessment) -> dict:
    """
    Scores an assessment based on stored response scores,
    updates Result.score_breakdown including section scores,
    track scores, total score, and skill gaps.
    """

    section_scores = {
        "verbal": 0,
        "logical": 0,
        "numerical": 0,
        "creative": 0,
        "empathy": 0,
    }

    responses = assessment.responses.select_related("question").all()

    for resp in responses:
        q = resp.question
        section_scores[q.section] += getattr(resp, "score", 0)

    track_scores = {
        "analytical": section_scores["logical"] + section_scores["numerical"],
        "communication": section_scores["verbal"],
        "creative": section_scores["creative"],
        "interpersonal": section_scores["empathy"],
    }

    total_score = sum(section_scores.values())

    primary_track, secondary_track = choose_primary_secondary_tracks(track_scores)

    mapped_profile = TRACK_TO_PROFILE.get(primary_track, "General")
    career_profile = CAREER_SKILL_PROFILES.get(mapped_profile, {})

    gaps = generate_gap_analysis(track_scores, career_profile)

    score_breakdown = {
        **section_scores,
        "tracks": track_scores,
        "total": total_score,
        "primary_track": primary_track,
        "secondary_track": secondary_track,
        "gaps": {g["skill"]: g for g in gaps},
    }

    Result.objects.update_or_create(
        user=assessment.user,
        defaults={
            "score_breakdown": score_breakdown,
            "primary_track": primary_track,
            "secondary_track": secondary_track,
            "scores": track_scores,
        },
    )

    return score_breakdown

# -----------------------------
# Track selection
# -----------------------------
def choose_primary_secondary_tracks(per_track_scores: Dict[str, float]) -> tuple[str, str]:
    items = sorted(per_track_scores.items(), key=lambda x: x[1], reverse=True)
    primary = items[0][0] if items else None
    secondary = items[1][0] if len(items) > 1 else None
    return primary, secondary

# -----------------------------
# Career recommendations
# -----------------------------
def recommend_careers(primary_track: str, limit=3):
    qs = Career.objects.filter(track__iexact=primary_track)
    if qs.exists():
        return list(qs[:limit])
    return list(Career.objects.all()[:limit])

# -----------------------------
# 5-year plan generation
# -----------------------------
def generate_five_year_plan_dynamic(per_track_scores: dict) -> list[dict]:
    if not per_track_scores:
        primary_track = "General"
        numeric_scores = {}
    else:
        numeric_scores = {}
        for k, v in per_track_scores.items():
            try:
                numeric_scores[k] = float(v)
            except (ValueError, TypeError):
                numeric_scores[k] = 0.0
        primary_track = max(numeric_scores.items(), key=lambda x: x[1])[0]

    track_goals = {
        "Data Science": [
            "Learn Python & statistics",
            "Work on small ML projects",
            "Contribute to open-source DS projects",
            "Take advanced ML/AI courses",
            "Lead data projects at work"
        ],
        "Software Engineering": [
            "Learn core programming & algorithms",
            "Build small projects",
            "Learn frameworks & best practices",
            "Contribute to team/open-source projects",
            "Lead engineering projects"
        ],
        "Logical": [
            "Practice logic puzzles and problem-solving",
            "Apply logic in coding/DS tasks",
            "Take advanced reasoning courses",
            "Mentor peers in problem-solving",
            "Lead complex projects requiring logical design"
        ],
        "General": [
            "Learn fundamentals",
            "Build projects",
            "Improve skills",
            "Gain professional experience",
            "Become a leader in field"
        ]
    }

    goals = track_goals.get(primary_track, track_goals["General"])

    total_score = sum(numeric_scores.values())
    max_score = len(numeric_scores) or 1
    percent = (total_score / max_score) * 100.0

    if percent < 50:
        goals[0] = f"Start with basics in {primary_track}"

    return [{"year": i + 1, "goal": g} for i, g in enumerate(goals)]
