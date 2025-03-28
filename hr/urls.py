from rest_framework import routers
from django.urls import path

from hr.views import GetResumeCPF, PositionViewSet, ProfileViewSet, ReportViewSet, ResumeViewSet, WorkExperienceViewSet, search_resumes, search_positions

router = routers.DefaultRouter()
router.register(r'resume', ResumeViewSet, basename='resume')
router.register(r'positions', PositionViewSet, basename='positions')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'report', ReportViewSet, basename='report')
router.register(r'work_experience', WorkExperienceViewSet, basename='work_experience')


urlpatterns = [
    path('get_resume_cpf', GetResumeCPF.as_view(), name='get_resume_cpf'),
    path("search_resumes", search_resumes, name="search_resumes"),
    path("search_positions", search_positions, name="search_positions"),
]

urlpatterns += router.urls