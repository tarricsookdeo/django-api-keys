from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    api_key = models.CharField(max_length=120, blank=True, null=True)
    api_secret = models.CharField(max_length=140, blank=True, null=True)

    def __str__(self):
        return self.email

    def has_valid_api_secret(self, secret_key: str) -> bool:
        return check_password(secret_key, self.api_secret)


@receiver(pre_save, sender=CustomUser)
def hash_api_secret(sender, instance, **kwargs):
    if instance.api_secret:
        instance.api_secret = make_password(instance.api_secret)


pre_save.connect(hash_api_secret, sender=CustomUser)
