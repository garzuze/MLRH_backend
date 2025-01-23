from django.db import models

class Client(models.Model):
    id                  = models.AutoField(primary_key=True)
    city                = models.CharField(max_length=45)  # cidade
    cnpj                = models.CharField(max_length=20, null=True, blank=True)  # cnpj
    state               = models.CharField(max_length=2)  # estado
    created             = models.DateTimeField(auto_now_add=True)  # created
    address             = models.CharField(max_length=45)  # endereco
    modified            = models.DateTimeField(auto_now=True)  # modified
    zip_code            = models.CharField(max_length=9, null=True, blank=True)  # cep
    trade_name          = models.CharField(max_length=144)  # nomeFantasia
    neighborhood        = models.CharField(max_length=45)  # bairro
    corporate_name      = models.CharField(max_length=144)  # razaoSocial
    state_registration  = models.CharField(max_length=20, null=True, blank=True)  # inscrEstadual
    number_of_employees = models.IntegerField(null=True, blank=True)  # numeroEmpregados

    class Meta:
        db_table = 'client'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
