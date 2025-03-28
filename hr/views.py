from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from hr.models import Position, Profile, Report, Resume, WorkExperience
from hr.permissions import IsAdminOrReadOnly
from hr.serializers import PositionSerializer, ProfileSerializer, ReportSerializer, ResumeSerializer, WorkExperienceSerializer

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
    queryset = Position.objects.all().order_by("title")
    serializer_class = PositionSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrReadOnly]


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
    
    def get_queryset(self):
        """
        If user is not superuser it only gets his resume
        """
        user = self.request.user
        if user.is_superuser:
            return Resume.objects.all()
        return Resume.objects.filter(user=user)
    

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAdminUser]


class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        resume = Resume.objects.filter(user=request.user).first()
        start_date = request.data.get('start_date')
        existing_experience = WorkExperience.objects.filter(resume=resume, start_date=start_date).first()
        # update it if it already exists
        if existing_experience:
            serializer = self.get_serializer(existing_experience, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        """
        If user is not superuser it only gets his work experience
        """
        user = self.request.user
        resume = Resume.objects.filter(user=user).first()
        if user.is_superuser:
            resume_id = self.request.query_params.get("resume")
            if resume_id:
                resume = Resume.objects.filter(id=resume_id).first()
                return WorkExperience.objects.filter(resume=resume)
            return WorkExperience.objects.all()
        return WorkExperience.objects.filter(resume=resume)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def search_resumes(request):
    query = request.GET.get("q", "")

    if query:
        resumes = Resume.objects.filter(name__icontains=query)[:5]
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)
    return Response([])

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_positions(request):
    query = request.GET.get("q", "")

    if query:
        positions = Position.objects.filter(title__icontains=query)[:5]
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)
    return Response([])