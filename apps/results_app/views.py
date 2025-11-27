# apps/results_app/views.py
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import viewsets, permissions
from sqlalchemy import TableSample
from .models import Result, Plan
from .serializers import ResultSerializer, PlanSerializer
from apps.assessment_app.services import TRACK_TO_PROFILE, score_assessment, choose_primary_secondary_tracks, recommend_careers
from apps.assessment_app.services import generate_five_year_plan_dynamic
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.contrib.auth.decorators import login_required
from apps.assessment_app.services import CAREER_SKILL_PROFILES

from apps.assessment_app.services import generate_skill_gaps_from_result


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

# HTML summary view
# apps/results_app/views.py
def map_track_to_career(track):
    TRACK_TO_CAREERS = {
        "analytical": ["Data Scientist", "Business Analyst", "AI Researcher"],
        "communication": ["Software Engineer", "Full-Stack Developer", "DevOps Engineer"],
        "creative": ["UI/UX Designer", "Product Designer"],
        "interpersonal": ["HR Specialist", "Project Coordinator", "Team Manager"],
        "management": ["Project Manager", "Product Manager", "Operations Manager"],
    }
    # Return the FIRST career as the "primary display"
    return TRACK_TO_CAREERS.get(track, ["General"])[0]


@login_required
def result_summary(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)
    score_breakdown = result.score_breakdown or {}
    tracks = score_breakdown.get("tracks", {})
    total = score_breakdown.get("total", 0)

    raw_primary = result.primary_track
    raw_secondary = result.secondary_track

    # MAPPED tracks shown to the user (Data Science, Design...)
    primary_career = map_track_to_career(raw_primary)
    secondary_career = map_track_to_career(raw_secondary)

     # Compute skill gaps
    skill_gaps = generate_skill_gaps_from_result(result,primary_career)

    # 5-year plan
    plan = generate_five_year_plan_dynamic(result.scores)

    

    # Recommended careers
    careers = recommend_careers(raw_primary, limit=3)

    return render(request, "results/summary.html", {
        "result": result,
        "primary_career": primary_career,
        "secondary_career": secondary_career,
        "careers": careers,
        "plan": plan,
        "skill_gaps": skill_gaps,
    })

# -----------------------------
# PDF Download View (outside the class)
# -----------------------------

# apps/results_app/views.py

@login_required
def download_plan_pdf(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)

    primary_track = result.primary_track or "analytical"  # fallback if missing
    careers_primary = TRACK_TO_PROFILE.get(primary_track, [])
    primary_career = careers_primary[0] if careers_primary else None

    # Skill gaps & 5-year plan
    skill_gaps = generate_skill_gaps_from_result(result, primary_career).get("gaps", [])
    plan = generate_five_year_plan_dynamic(result.scores)
    careers = recommend_careers(primary_track, limit=3)

    # PDF setup
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"Career Plan for {request.user.name}", styles['Title']))
    elements.append(Spacer(1, 12))

    # Track scores
    elements.append(Paragraph("Track Scores:", styles['Heading2']))
    for track, score in (result.scores or {}).items():
        elements.append(Paragraph(f"{track}: {score}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Skill Gap Analysis
    elements.append(Paragraph("Skill Gap Analysis:", styles['Heading2']))
    table_data = [["Skill", "Gap", "Action"]]
    for gap_item in skill_gaps:
        table_data.append([
            gap_item["skill"],
            str(gap_item["gap"]),
            gap_item["action"],
        ])
    table = Table(table_data, hAlign='LEFT', repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # 5-Year Development Plan
    elements.append(Paragraph("5-Year Development Plan:", styles['Heading2']))
    plan_list = ListFlowable(
        [ListItem(Paragraph(f"Year {item['year']}: {item['goal']}", styles['Normal']))
         for item in plan],
        bulletType='bullet', start='circle'
    )
    elements.append(plan_list)
    elements.append(Spacer(1, 12))

    # Recommended careers
    elements.append(Paragraph("Top Recommended Careers:", styles['Heading2']))
    for career in careers:
        elements.append(Paragraph(f"{career.title} – {career.description}", styles['Normal']))
        elements.append(Spacer(1, 6))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="career_plan_{result.id}.pdf"'
    return response

@login_required
def completed(request):
    results = Result.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "results/completed.html", {"results": results})
@login_required
def latest_summary(request):
    latest = Result.objects.filter(user=request.user).order_by('-created_at').first()
    if latest:
        return redirect('results_app:result_summary', result_id=latest.id)
    return redirect('results_app:completed')

