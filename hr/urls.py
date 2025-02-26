from rest_framework import routers
from django.urls import path

from hr.views import GetResume, GetResumeCPF

router = routers.DefaultRouter()
router.register(r'get_resume', GetResume, basename='resume')
urlpatterns = [
    path('get_resume_cpf', GetResumeCPF.as_view(), name='get_resume_cpf')
]

urlpatterns += router.urls