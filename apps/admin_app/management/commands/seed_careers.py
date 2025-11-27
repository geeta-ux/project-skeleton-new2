from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.careers_app.models import Career, CareerKB
from apps.results_app.models import Result, Plan
from apps.assessment_app.models import Assessment
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = "Seed careers, KB entries, demo user, sample assessment, results, and plans."

    def handle(self, *args, **kwargs):

        # -----------------------------------------------------------
        # 1️⃣ DEMO USER
        # -----------------------------------------------------------
        demo_user, created = User.objects.get_or_create(
            email="demo@example.com",
            defaults={
                "name": "demo",
                "password": "demo123",
            },
        )
        if created:
            demo_user.set_password("demo123")
            demo_user.save()
            self.stdout.write(self.style.SUCCESS("Created demo user: demo / demo123"))
        else:
            self.stdout.write(self.style.WARNING("Demo user already exists."))

        # -----------------------------------------------------------
        # 2️⃣ CAREER DATA
        # -----------------------------------------------------------
        careers_data = [
            {
                "title": "Data Scientist",
                "track": "data",
                "skills": ["Python", "Machine Learning", "Statistics", "SQL"],
                "description": "Analyze data to build predictive models.",
                "avg_salary_range": "8–30 LPA",
                "sample_roles": ["ML Engineer", "Data Analyst"],
            },
            {
                "title": "Full-Stack Developer",
                "track": "software",
                "skills": ["Python", "JavaScript", "React", "Django"],
                "description": "Build complete web applications.",
                "avg_salary_range": "6–25 LPA",
                "sample_roles": ["Backend Engineer", "Frontend Developer"],
            },
            {
                "title": "Cybersecurity Analyst",
                "track": "security",
                "skills": ["Networking", "Threat Analysis", "SIEM Tools"],
                "description": "Monitor and protect IT systems.",
                "avg_salary_range": "6–22 LPA",
                "sample_roles": ["SOC Analyst", "Security Engineer"],
            },
        ]

        for data in careers_data:
            # Use update_or_create to handle duplicates safely
            career, _ = Career.objects.update_or_create(
                title=data["title"],
                defaults=data
            )

        self.stdout.write(self.style.SUCCESS("Seeded careers."))

        # -----------------------------------------------------------
        # 3️⃣ CAREER KB DATA
        # -----------------------------------------------------------
        career_kb_data = [
            {
                "career": "Data Scientist",
                "title": "What skills are required?",
                "content": "A data scientist needs Python, machine learning, statistics, SQL.",
                "tags": ["skills", "data", "ml"]
            },
            {
                "career": "Full-Stack Developer",
                "title": "Roadmap to become full-stack",
                "content": "Learn HTML, CSS, JavaScript, React, Python, Django, Git.",
                "tags": ["roadmap", "webdev"]
            },
            {
                "career": "Cybersecurity Analyst",
                "title": "Beginner learning path",
                "content": "Start with networking basics, Linux, OWASP, SIEM tools.",
                "tags": ["security", "beginner"]
            },
        ]

        for kb in career_kb_data:
            career = Career.objects.get(title=kb["career"])
            CareerKB.objects.update_or_create(
                career=career,
                title=kb["title"],
                defaults={
                    "content": kb["content"],
                    "tags": kb["tags"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Seeded CareerKB."))

        # -----------------------------------------------------------
        # 4️⃣ DEMO ASSESSMENT + RESULT
        # -----------------------------------------------------------
        assessment, _ = Assessment.objects.get_or_create(
            user=demo_user,
            defaults={"completed_at": timezone.now()},
        )

        result, _ = Result.objects.get_or_create(
            user=demo_user,
            assessment=assessment,
            defaults={
                "scores": {
                    "logical": 78,
                    "numerical": 82,
                    "verbal": 74,
                    "technical": 85,
                },
                "primary_track": "software",
                "secondary_track": "data",
            },
        )

        self.stdout.write(self.style.SUCCESS("Seeded sample result."))

        # -----------------------------------------------------------
        # 5️⃣ PLANS DATA
        # -----------------------------------------------------------
        plans_data = [
            {
                "title": "Full-Stack Developer 3-Month Roadmap",
                "items": [
                    {"week": 1, "task": "Learn HTML, CSS"},
                    {"week": 2, "task": "JavaScript basics"},
                    {"week": 3, "task": "React fundamentals"},
                    {"week": 4, "task": "Backend with Django"},
                ],
            },
            {
                "title": "Data Science Beginner Path",
                "items": [
                    {"week": 1, "task": "Python basics"},
                    {"week": 2, "task": "Numpy & Pandas"},
                    {"week": 3, "task": "Statistics crash course"},
                    {"week": 4, "task": "ML essentials"},
                ],
            },
        ]

        for p in plans_data:
            Plan.objects.update_or_create(
                result=result,
                plan_json=p
            )

        # -----------------------------------------------------------
        # DONE
        # -----------------------------------------------------------
        self.stdout.write(self.style.SUCCESS("\nAll seeding completed successfully!"))
