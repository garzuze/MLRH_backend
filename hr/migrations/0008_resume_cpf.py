# Generated by Django 5.1.4 on 2025-02-24 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0007_rename_postal_code_resume_cep_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='cpf',
            field=models.CharField(default='123.456.789-10', max_length=14),
            preserve_default=False,
        ),
    ]
