from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from core.models import CustomUser
from hr.models import Position, Profile, Report, Resume, WorkExperience
from hr.permissions import IsAdminOrReadOnly
from hr.serializers import PositionSerializer, ProfileSerializer, ReportSerializer, ResumeSerializer, SlimProfileSerializer, SlimResumeSerializer, WorkExperienceSerializer

class GetResumeCPF(APIView):
    '''
    Receive CPF and return true if a resume with that cpf exists
    '''
    def get(self, request):
        cpf = request.query_params.get('cpf')
        user = CustomUser.objects.filter(cpf=cpf).first()
        
        if user:
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

    def get_queryset(self):
        """
        Clients can filter by status if wanted
        """
        status = self.request.query_params.get("status", None)
        if status:
            status_list = status.split(",")
            return Profile.objects.filter(status__in=status_list)
        
        return Profile.objects.all()
    

class SlimProfileViewSet(ProfileViewSet):
    queryset = Profile.objects.all()
    serializer_class = SlimProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class SlimResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = SlimResumeSerializer
    permission_classes = [permissions.IsAdminUser]

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
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

    def get_queryset(self):
        """
        Clients can filter by more than one id
        """
        status = self.request.query_params.get("id", None)
        if status:
            print("EU COMO COCO")
            status_list = status.split(",")
            return Report.objects.filter(id__in=status_list)
        
        return Report.objects.all()


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