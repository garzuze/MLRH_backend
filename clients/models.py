from django.db import models

class State(models.TextChoices):
    AC = 'AC', 'Acre'
    AL = 'AL', 'Alagoas'
    AM = 'AM', 'Amazonas'
    BA = 'BA', 'Bahia'
    CE = 'CE', 'Ceará'
    DF = 'DF', 'Distrito Federal'
    ES = 'ES', 'Espírito Santo'
    GO = 'GO', 'Goiás'
    MA = 'MA', 'Maranhão'
    MT = 'MT', 'Mato Grosso'
    MS = 'MS', 'Mato Grosso do Sul'
    MG = 'MG', 'Minas Gerais'
    PA = 'PA', 'Pará'
    PB = 'PB', 'Paraíba'
    PR = 'PR', 'Paraná'
    PE = 'PE', 'Pernambuco'
    PI = 'PI', 'Piauí'
    RJ = 'RJ', 'Rio de Janeiro'
    RN = 'RN', 'Rio Grande do Norte'
    RS = 'RS', 'Rio Grande do Sul'
    RO = 'RO', 'Rondônia'
    RR = 'RR', 'Roraima'
    SC = 'SC', 'Santa Catarina'
    SP = 'SP', 'São Paulo'
    SE = 'SE', 'Sergipe'
    TO = 'TO', 'Tocantins'


class Client(models.Model):
    id                  = models.AutoField(primary_key=True)
    cep                 = models.CharField(max_length=9, null=True, blank=True)
    city                = models.CharField(max_length=45)
    cnpj                = models.CharField(max_length=20, null=True, blank=True)
    state               = models.CharField(max_length=2, choices=State.choices, help_text="Abreviação do estado")    
    address             = models.CharField(max_length=45)
    trade_name          = models.CharField(max_length=144, help_text="Nome fantasia")
    created_at          = models.DateTimeField(auto_now_add=True)
    modified_at         = models.DateTimeField(auto_now=True)
    neighborhood        = models.CharField(max_length=45)
    corporate_name      = models.CharField(max_length=144, help_text="Razão Social")
    state_registration  = models.CharField(max_length=20, null=True, blank=True, help_text="Inscrição estadual")
    number_of_employees = models.IntegerField(null=True, blank=True, help_text="Número de empregados")

    class Meta:
        db_table = 'client'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def formatted_address(self):
        return f"{self.address}, {self.neighborhood}, {self.city} - {self.state}, {self.zip_code}"
    

class ClientContact(models.Model):
    '''Contatos dos clientes'''
    STATUS_CHOICES = [(True, "Ativo"), (False, "Inativo")]

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    status = models.BooleanField(choices=STATUS_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client_contact'
        verbose_name = 'Client Contact'
        verbose_name_plural = 'Client Contacts'
        ordering = ['name']


class Benefit(models.Model):
    benefit = models.CharField(max_length=50)