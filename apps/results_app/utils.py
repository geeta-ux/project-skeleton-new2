def generate_5_year_plan(result):
    """
    Generate normalized 5-year career plan.
    Output format matches UI + PDF expectations:
    [
        {
            "year": 1,
            "plan_json": {
                "title": "...",
                "items": ["...", "..."]
            }
        },
        ...
    ]
    """

    base_plan = [
        {
            "year": 1,
            "title": "Foundations Year",
            "items": [
                "Learn Python, SQL, and Git",
                "Complete at least 2 small projects",
                "Take an optional beginner certification"
            ],
        },
        {
            "year": 2,
            "title": "Project Development and Internship",
            "items": [
                "Build domain–specific projects",
                "Publish your public portfolio",
                "Secure an internship or entry-level role"
            ],
        },
        {
            "year": 3,
            "title": "Advanced Specialization",
            "items": [
                "Master advanced skills in your primary career track",
                "Complete certifications like Azure AI / DP-900 / AI-900",
                "Find an industry mentor"
            ],
        },
        {
            "year": 4,
            "title": "Impact & Visibility",
            "items": [
                "Work on cross-functional impact projects",
                "Start speaking, writing, or community contribution",
                "Improve soft-skills & leadership traits"
            ],
        },
        {
            "year": 5,
            "title": "Leadership or SME Path",
            "items": [
                "Transition towards lead/architect/SME role",
                "Negotiate salary or make a strategic role switch",
                "Establish thought leadership"
            ],
        },
    ]

    # Convert into {year: X, plan_json: {...}}
    final_plan = [
        {
            "year": p["year"],
            "plan_json": {
                "title": p["title"],
                "items": p["items"]
            }
        }
        for p in base_plan
    ]

    return final_plan
