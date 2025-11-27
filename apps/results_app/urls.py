from django.urls import path
from .views import latest_summary, result_summary, download_plan_pdf, completed

app_name = "results_app"

urlpatterns = [
    path('', completed, name='completed'),  # List of completed results
    path('summary/', latest_summary, name='latest_summary'),  # Latest result summary (no ID)
    path('summary/<int:result_id>/', result_summary, name='result_summary'),  # Specific result
    path('summary/<int:result_id>/download/', download_plan_pdf, name='download_plan_pdf'),
]
