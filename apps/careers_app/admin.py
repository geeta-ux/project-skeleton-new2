from django.contrib import admin
from .models import Career, CareerKB

class CareerKBInline(admin.TabularInline):
    model = CareerKB
    extra = 0

# @admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['id','title','track','avg_salary_range']
    inlines = [CareerKBInline]

admin.site.register(CareerKB)
