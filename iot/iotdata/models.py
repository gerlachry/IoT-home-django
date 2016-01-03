from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ReadingType(models.Model):
    reading_name = models.CharField(max_length=255, null=False, help_text='the name of the reading, ie. temperature, humidity, switch')

    def __unicode__(self):
        #needed this method which is used in the admin Feed change/add form for the drop down
        return self.reading_name


class FeedType(models.Model):
    feed_type = models.CharField(max_length=255, null=False, help_text='feed type')
    feed_desc = models.TextField(null=True, help_text='feed description')

    def __unicode__(self):
        return self.feed_type


class Feed(models.Model):
    feed_name = models.CharField(max_length=50, help_text='unique feed name to use when sending data to the api and looking up data also used as the index name')
    feed_desc = models.TextField(null=True, help_text='description of the feed')
    reading_type = models.ForeignKey(ReadingType, null=False, verbose_name='reading name')
    data_location = models.CharField(max_length=255, null=True, help_text='location info from where the data value originated from')
    feed_type = models.ForeignKey(FeedType, null=False)