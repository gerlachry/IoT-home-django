from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Device(models.Model):
    device_name = models.CharField(max_length=50, help_text='unique device id to use when sending data to the api and looking up data also used as the index name')
    device_desc = models.TextField(null=True, help_text='description of device')
    device_part_no = models.CharField(max_length=50, null=True, help_text='part number of device if available')
    device_location = models.CharField(max_length=255, null=True, help_text='location of device')