# apps/psychometric_app/pdf_utils.py

from reportlab.pdfgen import canvas

def generate_psychometric_pdf(response, profile):
    p = canvas.Canvas(response)

    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Psychometric Assessment Report")

    y = 760
    for key, value in profile.items():
        p.drawString(100, y, f"{key.replace('_',' ').title()}: {value}")
        y -= 30

    p.showPage()
    p.save()
