# Generated by Django 5.1.4 on 2025-02-25 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0011_alter_resume_unique_together_alter_resume_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='user',
        ),
    ]
