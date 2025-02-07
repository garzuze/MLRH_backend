from django.db import models

class AccountsPayableTitle(models.Model):
    """Título de contas a pagar."""
    issue_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Data de emissão do título."
    )

    supplier = models.CharField(
        max_length=100,
        null=True, 
        blank=True,
        help_text="Nome do fornecedor."
    )

    document_number = models.CharField(
        max_length=20,  
        unique=True,
        help_text="Número do documento referente ao título."
    )

    invoice_number = models.CharField(
        max_length=60,
        unique=True,
        help_text="Número do boleto ou fatura."
    )
    
    due_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Data de vencimento do título."
    )
    
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True, 
        blank=True,
        help_text="Valor do título."
    )
    
    description = models.CharField(
        max_length=100,
        null=True, 
        blank=True,
        help_text="Descrição breve do título."
    )

    payment_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Data em que o pagamento foi realizado."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora de criação do registro."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data e hora da última modificação do registro."
    )

    class Meta:
        verbose_name = "Título a pagar"
        verbose_name_plural = "Títulos a pagar"

    def __str__(self):
        return f"{self.document_number} - {self.supplier or 'Desconhecido'}"