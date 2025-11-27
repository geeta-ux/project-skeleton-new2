from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from .models import Career, CareerKB
from .serializers import CareerSerializer, CareerKBSerializer

# -----------------------------
# DRF API ViewSets
# -----------------------------
class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CareerKBViewSet(viewsets.ModelViewSet):
    queryset = CareerKB.objects.all()
    serializer_class = CareerKBSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# -----------------------------
# Web views for templates
# -----------------------------
def careers_list(request):
    """Render HTML list of careers"""
    careers = Career.objects.all()
    return render(request, "careers/list.html", {"careers": careers})

def career_detail(request, pk):
    """Render HTML detail page for a career"""
    career = get_object_or_404(Career, pk=pk)
    return render(request, "careers/detail.html", {"career": career})

def career_kb_detail(request, pk):
    """Render HTML detail page for a career knowledge base entry"""
    kb_entry = get_object_or_404(CareerKB, pk=pk)
    return render(request, "careers/kb_detail.html", {"kb_entry": kb_entry})
