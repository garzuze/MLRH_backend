from django.db import models

class Client(models.Model):
    id                  = models.AutoField(primary_key=True)
    cep                 = models.CharField(max_length=9, null=True, blank=True)
    city                = models.CharField(max_length=45)
    cnpj                = models.CharField(max_length=20, null=True, blank=True)
    state               = models.CharField(max_length=2)
    created             = models.DateTimeField(auto_now_add=True)
    address             = models.CharField(max_length=45)
    modified            = models.DateTimeField(auto_now=True)
    trade_name          = models.CharField(max_length=144, help_text="Nome fantasia")
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