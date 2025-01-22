from django.db import models

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    corporate_name = models.CharField(max_length=144)  # razaoSocial
    trade_name = models.CharField(max_length=144)  # nomeFantasia
    number_of_employees = models.IntegerField(null=True, blank=True)  # numeroEmpregados
    address = models.CharField(max_length=45)  # endereco
    neighborhood = models.CharField(max_length=45)  # bairro
    city = models.CharField(max_length=45)  # cidade
    state = models.CharField(max_length=2)  # estado
    zip_code = models.CharField(max_length=9, null=True, blank=True)  # cep
    cnpj = models.CharField(max_length=20, null=True, blank=True)  # cnpj
    state_registration = models.CharField(max_length=20, null=True, blank=True)  # inscrEstadual
    created = models.DateTimeField(null=True, blank=True)  # created
    modified = models.DateTimeField(null=True, blank=True)  # modified

    class Meta:
        db_table = 'client'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
