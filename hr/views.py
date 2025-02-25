from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, viewsets, status

from hr.models import Resume
from hr.serializers import ResumeSerializer

# Create your views here.

class GetResume(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return data associated
        with the currently authenticated user.
        """
        user = self.request.user
        return Resume.objects.filter(user=user)
