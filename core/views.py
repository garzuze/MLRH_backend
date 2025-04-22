import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from core.throttles import SignupRateThrottle
from hr.models import Position, Resume, WorkExperience

from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import permissions, viewsets, status
from rest_framework import generics
from rest_framework import status
from .utils import generate_email_verification_token


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email and password:
            raise self.fail("no_active_acount")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise self.fail("no_active_account")

        if not user.check_password(password):
            raise self.fail("no_active_account")

        if not user.is_active:
            raise self.fail("no_active_account")

        data = super().validate(attrs)
        data["user"] = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "cpf": user.cpf,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VerifyEmailAPIView(APIView):
    """
    Receive user's uid and token. If token matches with user, activate the user
    """

    def get(self, request):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")

        if not uid or not token:
            return Response(
                {"error": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, pk=uid)

        # If it matches, we can activate the user!
        if generate_email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {"message": "Email verified successfully.", "email": user.email}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def update_data(request):
    """Recuperar dados de sistema antigo a partir de arquivos JSON"""
    if request.method == "POST" and request.FILES["json_file"]:
        json_file = request.FILES["json_file"]
        data = json.load(json_file)
        for item in data:
            position_list = []
            for i in range(1, 4):
                position_list.append(item[f"cargoDesejado{i}_id"])
            print(position_list)
            resume = Resume.objects.get(phone=item["telefoneCelular"])
            print(resume)
            resume.desired_positions.add(*position_list)
            resume.save()

        return render(request, "clients/success.html")
    return render(request, "clients/form.html")
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def update_languages(request):
    for r in Resume.objects.all():
        if r.spanish_level == "1":
            r.spanish_level = "N"
        elif r.spanish_level == "2":
            r.spanish_level = "I"
        elif r.spanish_level == "3":
            r.spanish_level = "F"

        if r.english_level == "1":
            r.english_level = "N"
        elif r.english_level == "2":
            r.spanish_level = "I"
        elif r.english_level == "3":
            r.english_level = "F"

        r.save()

    return render(request, "clients/success.html")

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def update_resume(request):
    if request.method == "POST" and request.FILES["json_file"]:
        json_file = request.FILES["json_file"]
        data = json.load(json_file)
        marital_status = {
            "1": "S",
            "2": "M",
            "3": "D",
            "4": "W",
            "6": "M"
        }

        int_to_boolean = {
            "0": False,
            "1": True,
        }

        education_level = {
            "1": "EF",
            "2": "EF",
            "3": "EM",
            "4": "ET",
            "5": "GR",
            "6": "GR",
            "7": "PG",
            "8": "ME",
            "9": "DR",
            "10": "DR",
        }

        languages = {"1": "1", "2": "2", "3": "3", "4": "3"}

        for item in data:
            user, created = User.objects.update_or_create(
                email=item["email"], password=item["telefoneCelular"], cpf=item["cpf"], is_active=True
            )
            resume = Resume.objects.update_or_create(
                name=item["nome"],
                gender=item["sexo"],
                cnh=item["cnh"],
                birth_date=item["dataNascimento"],
                birth_place=item["localNascimento"],
                marital_status=marital_status[item["estadoCivil"]],
                spouse_name=item["nomeConjuge"],
                spouse_profession=item["profissaoConjuge"],
                has_children=int_to_boolean[item["temFilhos"]],
                children_ages=item["idadeFilhos"],
                is_smoker=int_to_boolean[item["fumante"]],
                has_car=int_to_boolean[item["possuiCarro"]],
                has_disability=int_to_boolean[item["pcd"]],
                disability_cid=item["cidPcd"],
                user=user,
                address=f"{item['endereco']} - {item['numero']} - {item['complemento']}",
                neighborhood=item["bairro"],
                city=item["cidade"],
                state=item["estado"],
                cep=item["cep"],
                phone=item["telefoneCelular"],
                contact_phone=item["telefoneRecado"],
                email=item["email"],
                education_level=education_level[item["nivelEscolaridade"]],
                education_details=item["formacao"],
                english_level=languages[item["idiomaIngles"]],
                spanish_level=languages[item["idiomaEspanhol"]],
                other_languages=item["idiomaOutros"],
                computer_skills=item["informatica"],
                additional_courses=item["outrosCursos"],
                expected_salary=item["pretensaoSalarial"],
                available_full_time=int_to_boolean[item["dispHorarioComercial"]],
                available_morning_afternoon=int_to_boolean[item["dispManhaTarde"]],
                available_afternoon_night=int_to_boolean[item["dispTardeNoite"]],
                available_night_shift=int_to_boolean[item["dispMadrugada"]],
                available_1236=int_to_boolean[item["disp1236"]],
                available_as_substitute=int_to_boolean[item["dispFolguista"]],
            )
            position_list = []
            for i in range(1, 4):
                try:
                    position = Position.objects.get(id=item[f"cargoDesejado{i}_id"])
                    print(position)
                    if position != None:
                        position_list.append(item[f"cargoDesejado{i}_id"])
                except Position.DoesNotExist:
                    print(f"não existe: {item[f'cargoDesejado{i}_id']}")
                    
            resume = Resume.objects.get(phone=item["telefoneCelular"])
            print(resume)
            print(position_list)
            resume.desired_positions.add(*position_list)
            resume.save()
            for i in range(1, 4):
                 experience, created = WorkExperience.objects.update_or_create(
                     resume=resume,
                     company_name=item[f"empresa{i}"],
                     position_title=item[f"funcao{i}"],
                     start_date=item[f"dataAdmissao{i}"],
                     end_date=item[f"dataDemissao{i}"],
                     salary=item[f"salario{i}"],
                     responsibilities=item[f"atividades{i}"],
                     reason_for_leaving=item[f"motivoSaida{i}"],)
                 print(experience)

        return render(request, "clients/success.html")
    return render(request, "clients/form.html")


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    throttle_classes = [SignupRateThrottle]
