from django.db import models
from django.conf import settings

# Since we are generating questions dynamically, we store the *result* 
# which contains the questions generated for that specific session.

class CareerAssessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    
    # Store the generated questions as JSON so we know what was asked
    # Structure: [{"id": 1, "text": "...", "options": [...], "correct": "..."}]
    questions_data = models.JSONField(default=list) 
    
    # Store user's answers
    # Structure: {"1": "Option A", "2": "Option C"}
    answers_data = models.JSONField(default=dict)
    
    # Store final scores per category
    # Structure: {"Logical": 8, "Verbal": 7, ...}
    scores = models.JSONField(default=dict)

    # Store AI generated insights (Skill-gap, 5-year plan, recommended careers)
    insights = models.JSONField(default=dict)
    
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Assessment for {self.user} on {self.date_taken}"

