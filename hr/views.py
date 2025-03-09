from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView

from hr.models import Position, Resume
from hr.serializers import PositionSerializer, ResumeSerializer

class GetResumeCPF(APIView):
    '''
    Receive CPF and return true if a resume with that cpf exists
    '''
    def get(self, request):
        cpf = request.query_params.get('cpf')
        
        resume = Resume.objects.filter(cpf=cpf).first()
        
        if resume:
            return Response({"message": True}, status=status.HTTP_200_OK)
        else:
            return Response({"message": False}, status=status.HTTP_204_NO_CONTENT)


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAdminUser]


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


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cpf = request.data.get('cpf')
        existing_resume = Resume.objects.filter(user=request.user, cpf=cpf).first()
        if existing_resume:
            serializer = self.get_serializer(existing_resume, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return super().create(request, *args, **kwargs)