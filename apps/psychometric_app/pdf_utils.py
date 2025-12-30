from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def generate_psychometric_pdf(response, profile):
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    margin_left = 20 * mm
    margin_top = height - 20 * mm
    line_gap = 8 * mm
    y = margin_top

    # --- Title ---
    p.setFont("Helvetica-Bold", 18)
    p.drawString(margin_left, y, "Psychometric Assessment Report")
    y -= 15 * mm

    # --- Profile Summary ---
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin_left, y, "Profile Summary")
    y -= 10 * mm

    p.setFont("Helvetica", 12)
    p.drawString(margin_left, y, f"Personality Level: {profile.get('personality_level', '-')}")
    y -= line_gap
    p.drawString(margin_left, y, f"Interest Type: {profile.get('interest_type', '-')}")
    y -= line_gap
    p.drawString(margin_left, y, f"Value Orientation: {profile.get('value_orientation', '-')}")
    y -= 20

    # --- Recommended Careers ---
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin_left, y, "Recommended Careers")
    y -= 10 * mm

    careers = profile.get("recommended_careers", [])

    p.setFont("Helvetica", 12)

    if careers:
        for career in careers:
            # Handle string or dict
            if isinstance(career, dict):
                title = career.get("title", "-")
                category = career.get("category", "-")
                text = f"• {title} ({category})"
            else:
                text = f"• {career}"

            # Wrap to next page if needed
            if y < 25 * mm:
                p.showPage()
                y = margin_top
                p.setFont("Helvetica", 12)

            p.drawString(margin_left + 10, y, text)
            y -= line_gap
    else:
        p.drawString(margin_left + 10, y, "No mapped careers yet.")
        y -= line_gap

    # --- Footer ---
    if y < 50:
        p.showPage()
        y = margin_top

    p.setFont("Helvetica-Oblique", 10)
    p.drawString(margin_left, 15 * mm, "This report provides insight into your personality, interests, and values.")

    p.showPage()
    p.save()
