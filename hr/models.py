from django.db import models
from django.contrib.auth import get_user_model

from clients.models import Client, ClientContact, ClientFee, State
User = get_user_model()


class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"


class MaritalStatus(models.TextChoices):
    SINGLE = "S", "Solteiro(a)"
    MARRIED = "M", "Casado(a)"
    DIVORCED = "D", "Divorciado(a)"
    WIDOWED = "V", "Viúvo(a)"


class EducationLevel(models.TextChoices):
    EF = "EF", "Ensino Fundamental"
    EM = "EM", "Ensino Médio"
    ET = "ET", "Ensino Médio Técnico"
    TE = "TE", "Tecnólogo"
    GR = "GR", "Graduação"
    PG = "PG", "Pós-graduação"
    ME = "ME", "Mestrado"
    DR = "DR", "Doutorado"


class Gender(models.TextChoices):
    M = "M", "Masculino"
    F = "F", "Feminino"
    O = "O", "Outro"


class Resume(models.Model):
    '''Currículo de um candidato'''
    LANGUAGE_LEVEL_CHOICES = [
        (1, "Básico"),
        (2, "Intermediário"),
        (3, "Fluente"),
    ]

    STATUS_CHOICES = [
        ("A", "Ativo"),
        ("I", "Inativo")
    ]

    name = models.CharField(max_length=60)
    cpf = models.CharField(max_length=14, unique=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=45)
    marital_status = models.CharField(
        choices=MaritalStatus.choices,
        max_length=1,
        help_text="Estado civil")
    spouse_name = models.CharField(
        max_length=45, null=True, blank=True, help_text="Nome cônjuge")
    spouse_profession = models.CharField(max_length=45, null=True, blank=True)
    has_children = models.BooleanField(null=True, blank=True)
    children_ages = models.CharField(max_length=20, null=True, blank=True)
    is_smoker = models.BooleanField(default=False)
    has_car = models.BooleanField(default=False)
    has_disability = models.BooleanField(default=False)
    disability_cid = models.CharField(max_length=10, null=True, blank=True)
    user = models.OneToOneField(User, verbose_name="Usuário", on_delete=models.CASCADE, unique=True)

    # Contact Info
    address = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    state = models.CharField(
        max_length=2, choices=State.choices, help_text="Abreviação do estado")
    cep = models.CharField(max_length=9)
    phone = models.CharField(max_length=15)
    contact_phone = models.CharField(
        max_length=15, null=True, blank=True, help_text="Telefone para contato")
    email = models.EmailField(max_length=100)
    linkedin = models.URLField(null=True, blank=True)

    # Education & Skills
    education_level = models.CharField(
        choices=EducationLevel.choices,
        max_length=2,
        help_text="Nível de escolaridade"
    )
    education_details = models.TextField()
    english_level = models.IntegerField(choices=LANGUAGE_LEVEL_CHOICES)
    spanish_level = models.IntegerField(choices=LANGUAGE_LEVEL_CHOICES)
    other_languages = models.CharField(max_length=45, null=True, blank=True)
    computer_skills = models.TextField(null=True, blank=True)
    additional_courses = models.TextField(null=True, blank=True)

    # Desired positions
    desired_positions = models.ManyToManyField(
        Position, related_name="resumes", blank=True)
    expected_salary = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)

    # Availability
    available_full_time = models.BooleanField(
        default=False, help_text="Horário comercial")
    available_morning_afternoon = models.BooleanField(
        default=False, help_text="Manhã - Tarde")
    available_afternoon_night = models.BooleanField(
        default=False, help_text="Tarde - Noite")
    available_night_shift = models.BooleanField(
        default=False, help_text="Madrugada")
    available_1236 = models.BooleanField(
        default=False, help_text="Escala 12x36")
    available_as_substitute = models.BooleanField(
        default=False, help_text="Folguista")

    # Status & Timestamps
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Currículo"
        verbose_name_plural = "Currículos"


class WorkExperience(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="work_experiences")
    company_name = models.CharField(max_length=100)
    position_title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    responsibilities = models.TextField()
    reason_for_leaving = models.CharField(
        max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.position_title} na {self.company_name}"

    class Meta:
        verbose_name = "Experiência"
        verbose_name_plural = "Experiências"


class ProfileStatus(models.TextChoices):
    ACTIVE = "A", "Ativo"
    INACTIVE = "I", "Inativo"
    CANCELED = "C", "Cancelado"
    SUSPENDED = "S", "Suspenso"


class Profile(models.Model):
    """Perfil de uma vaga ou posição dentro de uma empresa."""
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="profiles",
        help_text="Cliente associado a este perfil.",
        default=1
    )

    client_contact = models.ForeignKey(
        ClientContact,
        on_delete=models.PROTECT,
        related_name="profiles",
        help_text="Contato dentro da empresa cliente.",
        default=1
    )

    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="profiles",
        help_text="Cargo associado ao perfil.",
        default=1,
    )

    fee = models.ForeignKey(
        ClientFee,
        on_delete=models.PROTECT,
        related_name="profiles",
        help_text="Honorário associado ao serviço.",
        default=1
    )

    date = models.DateField(
        null=True,
        blank=True,
        help_text="Data de criação do perfil."
    )

    status = models.CharField(
        max_length=1,
        choices=ProfileStatus.choices,
        default=ProfileStatus.ACTIVE,
        help_text="Status do perfil: Ativo (A), Inativo (I), Cancelado (C) ou Suspenso (S)."
    )

    deadline = models.IntegerField(
        null=True,
        blank=True,
        help_text="Prazo para preenchimento da vaga (em dias)."
    )

    estimated_delivery = models.DateField(
        null=True,
        blank=True,
        help_text="Previsão de entrega do perfil ao cliente."
    )

    confidential = models.BooleanField(
        null=True,
        blank=True,
        help_text="Se marcado, indica que a vaga é sigilosa."
    )

    quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Quantidade de posições disponíveis para este perfil."
    )

    remuneration = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Remuneração oferecida para a vaga."
    )

    service_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor do serviço de recrutamento."
    )

    title_generated = models.BooleanField(
        default=False,
        help_text="Indica se o título para esta vaga já foi gerado."
    )

    work_schedule = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Horário e frequência de trabalho para a vaga."
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Idade mínima recomendada para a vaga."
    )

    marital_status = models.CharField(
        choices=MaritalStatus.choices,
        help_text="Estado civil do candidato desejado.",
        max_length=1
    )

    gender = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=Gender.choices,
        help_text="Gênero do candidato desejado."
    )

    education_level = models.CharField(
        choices=EducationLevel.choices,
        max_length=2,
        help_text="Nível de escolaridade exigido para a vaga."
    )

    computer_skills = models.TextField(
        blank=True,
        help_text="Habilidades em informática necessárias para a vaga."
    )

    languages = models.CharField(
        max_length=45,
        null=True,
        blank=True,
        help_text="Idiomas exigidos ou desejáveis para a vaga."
    )

    job_responsibilities = models.TextField(
        blank=True,
        help_text="Principais atividades e responsabilidades da posição."
    )

    professional_experience = models.TextField(
        blank=True,
        help_text="Experiência profissional exigida para a posição."
    )

    behavioral_profile = models.TextField(
        blank=True,
        help_text="Perfil comportamental desejado para o candidato."
    )

    work_environment = models.TextField(
        blank=True,
        help_text="Características do local de trabalho."
    )

    additional_notes = models.TextField(
        blank=True,
        help_text="Observações gerais sobre a vaga."
    )

    restrictions = models.TextField(
        blank=True,
        help_text="Restrições ou requisitos especiais para a posição."
    )

    cancellation_reason = models.TextField(
        blank=True,
        help_text="Motivo do cancelamento da vaga, se aplicável."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora de criação do perfil."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data e hora da última modificação no perfil."
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f"{self.position.name} - {self.client.name}"

class Report(models.Model):
    '''Parecer de uma vaga'''
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, default=1)
    resume = models.ForeignKey(Resume, on_delete=models.PROTECT, default=1)

    test_result = models.TextField(blank=True)
    personal_family_context = models.TextField(blank=True)
    educational_background = models.TextField(blank=True)
    professional_summary = models.TextField(blank=True)
    candidate_profile = models.TextField(blank=True)
    career_objectives = models.TextField(blank=True)
    final_considerations = models.TextField(blank=True)

    agreed_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=0.00
    )

    candidate_start_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Parecer"
        verbose_name_plural = "Pareceres"

    def __str__(self):
        return f" {self.candidate.name} - Status: {self.get_status_display()}"
