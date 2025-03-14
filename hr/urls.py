from rest_framework import routers
from django.urls import path

from hr.views import GetResume, GetResumeCPF, PositionViewSet, ProfileViewSet, ReportViewSet, ResumeViewSet, WorkExperienceViewSet, search_resumes

router = routers.DefaultRouter()
router.register(r'get_resume', GetResume, basename='get_resume')
router.register(r'resume', ResumeViewSet, basename='resume')
router.register(r'positions', PositionViewSet, basename='positions')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'report', ReportViewSet, basename='report')
router.register(r'work_experience', WorkExperienceViewSet, basename='work_experience')


urlpatterns = [
    path('get_resume_cpf', GetResumeCPF.as_view(), name='get_resume_cpf'),
    path("search_resumes", search_resumes, name="search_resumes"),
]

urlpatterns += router.urls