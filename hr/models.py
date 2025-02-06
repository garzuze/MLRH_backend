from django.db import models


class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Resume(models.Model):
    GENDER_CHOICES = [("M", "Masculino"), ("F", "Feminino"), ("O", "Outro")]
    MARITAL_STATUS_CHOICES = [
        (1, "Solteiro(a)"),
        (2, "Casado(a)"),
        (3, "Divorciado(a)"),
        (4, "Viúvo(a)"),
    ]

    EDUCATION_LEVEL_CHOICES = [
        (1, "Ensino Fundamental"),
        (2, "Ensino Médio"),
        (3, "Ensino Médio Técnico"),
        (4, "Tecnólogo"),
        (5, "Graduação"),
        (6, "Pós-graduação"),
        (7, "Mestrado"),
        (8, "Doutorado"),
    ]

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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=45)
    marital_status = models.IntegerField(choices=MARITAL_STATUS_CHOICES)
    spouse_name = models.CharField(
        max_length=45, null=True, blank=True, help_text="Nome cônjuge")
    spouse_profession = models.CharField(max_length=45, null=True, blank=True)
    has_children = models.BooleanField(null=True, blank=True)
    children_ages = models.CharField(max_length=20, null=True, blank=True)
    is_smoker = models.BooleanField(default=False)
    has_car = models.BooleanField(default=False)
    has_disability = models.BooleanField(default=False)
    disability_cid = models.CharField(max_length=10, null=True, blank=True)

    # Contact Info
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=6)
    complement = models.CharField(max_length=20, null=True, blank=True)
    neighborhood = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    postal_code = models.CharField(max_length=9)
    phone = models.CharField(max_length=15)
    contact_phone = models.CharField(max_length=15, null=True, blank=True, help_text="Telefone para contato")
    email = models.EmailField(max_length=100)
    linkedin = models.URLField(null=True, blank=True)

    # Education & Skills
    education_level = models.IntegerField(choices=EDUCATION_LEVEL_CHOICES)
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
