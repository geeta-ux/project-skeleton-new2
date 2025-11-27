# apps/results_app/serializers.py
from rest_framework import serializers
from .models import Result, Plan
from apps.assessment_app.services import generate_gap_analysis, generate_five_year_plan_dynamic, CAREER_SKILL_PROFILES

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['year', 'plan_json']  # Only expose what we need

class ResultSerializer(serializers.ModelSerializer):
    # Embed saved plans
    plans = PlanSerializer(many=True, read_only=True)

    # Skill gaps computed dynamically
    skill_gaps = serializers.SerializerMethodField()
    # Dynamic 5-year plan
    five_year_plan = serializers.SerializerMethodField()
    # UI-ready JSON for frontend
    ui = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = [
            'id',
            'user',
            'assessment',
            'scores',
            'primary_track',
            'secondary_track',
            'created_at',
            'plans',
            'skill_gaps',
            'five_year_plan',
            'ui',
        ]
        read_only_fields = ['user', 'plans']

    def get_skill_gaps(self, obj):
        try:
            # Determine career profile based on primary track
            mapped_profile = obj.primary_track or "General"
            career_profile = CAREER_SKILL_PROFILES.get(mapped_profile, {})
            return generate_gap_analysis(obj.scores or {}, career_profile)
        except Exception:
            return []

    def get_five_year_plan(self, obj):
        try:
            return generate_five_year_plan_dynamic(obj.scores or {})
        except Exception:
            return []

    def get_ui(self, obj):
        score = obj.scores or {}
        return {
            "header": {
                "primary_track": obj.primary_track,
                "secondary_track": obj.secondary_track,
                "total_score": sum(score.values()) if score else 0,
            },
            "radar_scores": [
                {"axis": "Analytical", "value": score.get("analytical", 0)},
                {"axis": "Communication", "value": score.get("communication", 0)},
                {"axis": "Creative", "value": score.get("creative", 0)},
                {"axis": "Interpersonal", "value": score.get("interpersonal", 0)},
            ],
            "gaps": self.get_skill_gaps(obj),
            "plan": self.get_five_year_plan(obj),
        }
