# Generated by Django 5.1.4 on 2025-02-07 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_alter_benefit_options_alter_client_options_clientfee'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='benefits',
            field=models.ManyToManyField(related_name='clients', to='clients.benefit'),
        ),
        migrations.AlterField(
            model_name='benefit',
            name='benefit',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
