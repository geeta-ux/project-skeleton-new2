from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.users_app.views import UserViewSet
from apps.assessment_app.views import QuestionViewSet, AssessmentViewSet, ResponseViewSet
from apps.results_app.views import ResultViewSet, PlanViewSet
from apps.careers_app.views import CareerViewSet, CareerKBViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from career_guide.views import base

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'responses', ResponseViewSet)
router.register(r'results', ResultViewSet)
router.register(r'plans', PlanViewSet)
router.register(r'careers', CareerViewSet)
router.register(r'career-kb', CareerKBViewSet)

urlpatterns = [ path('', base, name='base'), 
               path('admin/', admin.site.urls), 
               path("accounts/", include("allauth.urls")), 

               path('api/', include(router.urls)), 
               path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
               path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
               path('auth/', include('apps.users_app.urls')), # <-- add this 
               path("assessment/", include("apps.assessment_app.urls")), 
               path('results/', include('apps.results_app.urls', namespace='results_app')), 
               path("careers/", include("apps.careers_app.urls")), # ✅ add this 
               path('psychometric/', include(('apps.psychometric_app.learning.urls', 'psychometric'),namespace='psychometric')),
               
               # Compatibility layer for cached JS calling /api/
               path('api/', include('apps.psychometric_app.learning.urls')),
               ]

