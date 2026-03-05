from django.contrib import admin
from .models import CareerAssessment

@admin.register(CareerAssessment)
class CareerAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_taken', 'completed')
    list_filter = ('completed', 'date_taken')
    search_fields = ('user__email', 'user__name')
