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
    "analytical": [
        "Data Scientist",
        "Business Analyst",
        "AI Researcher"
    ],

    "communication": [
        "Software Engineer",
        "Full-Stack Developer",
        "DevOps Engineer"
    ],

    "creative": [
        "UI/UX Designer",
        "Product Designer"
    ],

    "interpersonal": [
        "HR Specialist",
        "Customer Success Manager",
        "Career Coach",
        "Client Relationship Manager"
    ],

    "management": [
        "Project Manager",
        "Product Manager",
        "Operations Manager",
        "Team Lead"
    ]
}


# -----------------------------
# Career Skill Profiles
# -----------------------------
CAREER_SKILL_PROFILES = {
    "Data Scientist": {
        "python": 5,
        "statistics": 5,
        "machine_learning": 5,
        "data_visualization": 4,
        "communication": 3,
    },
    "Business Analyst": {
        "excel": 5,
        "data_analysis": 5,
        "sql": 4,
        "critical_thinking": 4,
        "communication": 4,
    },
    "AI Researcher": {
        "python": 5,
        "machine_learning": 5,
        "deep_learning": 5,
        "math": 5,
        "research": 4,
    },
    "Software Engineer": {
        "programming": 5,
        "algorithms": 5,
        "system_design": 4,
        "databases": 4,
        "communication": 3,
    },
    "Full-Stack Developer": {
        "frontend": 4,
        "backend": 4,
        "databases": 4,
        "api_design": 4,
        "devops_basics": 3,
    },
    "DevOps Engineer": {
        "linux": 5,
        "cloud": 4,
        "automation": 4,
        "ci_cd": 4,
        "scripting": 4,
    },
    "UI/UX Designer": {
        "figma": 5,
        "design_thinking": 5,
        "user_research": 4,
        "visual_design": 4,
        "creativity": 5,
    },
    "Product Designer": {
        "ui_design": 4,
        "ux_design": 5,
        "research": 4,
        "prototyping": 5,
        "visual_design": 4,
    },
    "HR Specialist": {
        "communication": 5,
        "empathy": 5,
        "conflict_resolution": 4,
        "organization": 4,
    },
    "Career Coach": {
        "empathy": 5,
        "communication": 5,
        "counseling": 5,
        "goal_setting": 4,
    },
    "Customer Success Manager": {
        "relationship_management": 5,
        "communication": 5,
        "empathy": 5,
        "crm_tools": 4,
    },
    "Project Manager": {
        "leadership": 5,
        "project_management": 5,
        "agile_scrum": 4,
        "communication": 5,
        "risk_management": 4,
    },
    "Product Manager": {
        "strategic_thinking": 5,
        "communication": 5,
        "market_research": 4,
        "roadmapping": 4,
        "data_analysis": 3,
    },
}
# -----------------------------
# Skill → Track mapping & inference helpers
# -----------------------------
SKILL_TO_TRACK = {
    "python": "analytical",
    "statistics": "analytical",
    "machine_learning": "analytical",
    "data_visualization": "analytical",
    "excel": "analytical",
    "data_analysis": "analytical",
    "sql": "analytical",

    "programming": "communication",
    "algorithms": "communication",
    "system_design": "communication",
    "databases": "communication",

    "figma": "creative",
    "design_thinking": "creative",
    "visual_design": "creative",
    "user_research": "creative",

    "empathy": "interpersonal",
    "communication": "interpersonal",
    "conflict_resolution": "interpersonal",

    "leadership": "management",
    "project_management": "management",
    "agile_scrum": "management",
}

def infer_skill_scores_from_track_scores(track_scores: dict, career_profile: dict) -> dict:
    """
    Heuristic to estimate user's per-skill score (0..5) from their track scores.

    - track_scores: {'analytical': 12, 'communication': 6, ...}
    - career_profile: {'python': 5, 'statistics': 5, ...}

    For each skill in career_profile:
      - if SKILL_TO_TRACK maps it to a track, use that track's score (normalized).
      - otherwise use average of all tracks.
    """
    # ensure numeric
    numeric_track_scores = {}
    for t, v in track_scores.items():
        try:
            numeric_track_scores[t] = float(v)
        except (TypeError, ValueError):
            numeric_track_scores[t] = 0.0

    max_track_val = max(numeric_track_scores.values()) if numeric_track_scores else 1.0
    max_track_val = max(1.0, max_track_val)

    # compute average if needed (prevent division by zero)
    avg_track = (sum(numeric_track_scores.values()) / len(numeric_track_scores)) if numeric_track_scores else 0.0

    skill_estimates = {}
    for skill in career_profile.keys():
        key = skill.lower().replace(" ", "_")
        mapped_track = SKILL_TO_TRACK.get(key)
        if mapped_track and mapped_track in numeric_track_scores:
            raw = numeric_track_scores.get(mapped_track, 0.0)
        else:
            raw = avg_track

        # normalize raw to 0..5
        est = (raw / max_track_val) * 5.0
        skill_estimates[skill] = round(est, 2)

    return skill_estimates


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
def generate_skill_gaps_from_result(result, career_name):
    required_skills = CAREER_SKILL_PROFILES.get(career_name, {})
    user_scores = result.scores or {}

    gaps = []

    for skill, required in required_skills.items():
        current = user_scores.get(skill, 0)
        gap = round(required - current, 2)

        gaps.append({
            "skill": skill,
            "gap": max(gap, 0),
            "action": "Upskill required" if gap > 0 else "No action needed",
        })

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
    careers_primary = TRACK_TO_PROFILE.get(primary_track, [])
    careers_secondary = TRACK_TO_PROFILE.get(secondary_track, [])

    primary_career = careers_primary[0] if careers_primary else None
    career_profile = CAREER_SKILL_PROFILES.get(primary_career, {})

    user_skill_estimates = infer_skill_scores_from_track_scores(track_scores, career_profile)
    gaps = generate_gap_analysis(user_skill_estimates, career_profile)

    score_breakdown = {
        **section_scores,
        "tracks": track_scores,
        "total": total_score,
        "primary_track": primary_track,
        "secondary_track": secondary_track,
        "primary_careers": careers_primary,
        "secondary_careers": careers_secondary,
        "gaps": {g["skill"]: g for g in gaps},
    }

    Result.objects.update_or_create(
        user=assessment.user,
        assessment=assessment,
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
    qs = Career.objects.filter(track__contains=[primary_track])
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
        primary_career = TRACK_TO_PROFILE.get(primary_track, ["General"])[0]


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

    goals = track_goals.get(primary_career, track_goals["General"])

    total_score = sum(numeric_scores.values())
    max_score = len(numeric_scores) or 1
    percent = (total_score / max_score) * 100.0

    if percent < 50:
        goals[0] = f"Start with basics in {primary_career}"

    return [{"year": i + 1, "goal": g} for i, g in enumerate(goals)]
