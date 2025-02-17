from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=User)
def set_username_as_email(sender, instance, **kwargs):
    """Ensure username is always set to email before saving"""
    if not instance.username:
        instance.username = instance.email