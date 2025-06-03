from django.db import models

from clients.models import Client, ClientContact
from hr.models import Profile, Report


class PayableTitle(models.Model):
    """Título de contas a pagar."""

    issue_date = models.DateField(
        null=True, blank=True, help_text="Data de emissão do título."
    )

    supplier = models.CharField(
        max_length=100, null=True, blank=True, help_text="Nome do fornecedor."
    )

    document_number = models.CharField(
        max_length=20, unique=True, help_text="Número do documento referente ao título."
    )

    invoice_number = models.CharField(
        max_length=60, unique=True, help_text="Número do boleto ou fatura."
    )

    due_date = models.DateField(
        null=True, blank=True, help_text="Data de vencimento do título."
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor do título.",
    )

    description = models.CharField(
        max_length=100, null=True, blank=True, help_text="Descrição breve do título."
    )

    payment_date = models.DateField(
        null=True, blank=True, help_text="Data em que o pagamento foi realizado."
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Data e hora de criação do registro."
    )

    updated_at = models.DateTimeField(
        auto_now=True, help_text="Data e hora da última modificação do registro."
    )

    class Meta:
        verbose_name = "Título a pagar"
        verbose_name_plural = "Títulos a pagar"

    def __str__(self):
        return f"{self.document_number} - {self.supplier or 'Desconhecido'}"


class ReceivableTitle(models.Model):
    """Título de contas a receber."""

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="receivable_titles",
        help_text="Cliente associado ao título.",
    )

    client_contact = models.ForeignKey(
        ClientContact,
        on_delete=models.PROTECT,
        related_name="receivable_titles",
        help_text="Contato do cliente"
    )

    reports = models.ManyToManyField(
        Report,
        related_name="receivable_titles",
        help_text="Parecer associado ao título",
    )


    document = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        help_text="Número do documento associado ao título.",
    )

    due_date = models.DateField(
        null=True, blank=True, help_text="Data de vencimento do título."
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor do título.",
    )

    payment_date = models.DateField(
        null=True, blank=True, help_text="Data em que o pagamento foi realizado."
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Data e hora de criação do registro."
    )

    updated_at = models.DateTimeField(
        auto_now=True, help_text="Data e hora da última modificação do registro."
    )

    class Meta:
        verbose_name = "Título a receber"
        verbose_name_plural = "Títulos a receber"
        ordering = ("-updated_at", )

    def __str__(self):
        return f"{self.document or 'Sem documento'} - {self.client.trade_name} - R$ {self.amount}"
