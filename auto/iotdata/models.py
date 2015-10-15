from django.db import models

class Locations(models.Model):
    name = models.CharField(max_length=255);
    active = models.BooleanField();
    create_date = models.DateTimeField('date record was created');
    modified_date = models.DateTimeField('date record was last modified');


class Sensors(models.Model):
    device_id = models.CharField(max_length=255);
    location_id = models.ForeignKey(Locations);
    name = models.CharField(max_length=255);
    purchased_from = models.CharField(max_length=255);
    manufacturer = models.CharField(max_length=255);
    active = models.BooleanField();
    create_date = models.DateTimeField('date record was created');
    modified_date = models.DateTimeField('date record was last modified');


class ReadingType(models.Model):
    name = models.CharField(max_length=255);
    active = models.BooleanField();
    create_date = models.DateTimeField('date record was created');
    modified_date = models.DateTimeField('date record was last modified');

class Readings(models.Model):
    sensor_id = models.ForeignKey(Sensors);
    reading_type_id = models.ForeignKey(ReadingType);
    value = models.TextField();
    info = models.TextField();
    create_date = models.DateTimeField();

