# Generated by Django 5.1.4 on 2025-02-15 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_alter_client_benefits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='number_of_employees',
            field=models.PositiveIntegerField(blank=True, help_text='Número de empregados', null=True),
        ),
    ]
