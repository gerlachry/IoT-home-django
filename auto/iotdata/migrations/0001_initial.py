# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField()),
                ('create_date', models.DateTimeField(verbose_name=b'date record was created')),
                ('modified_date', models.DateTimeField(verbose_name=b'date record was last modified')),
            ],
        ),
        migrations.CreateModel(
            name='Readings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('info', models.TextField()),
                ('create_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ReadingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField()),
                ('create_date', models.DateTimeField(verbose_name=b'date record was created')),
                ('modified_date', models.DateTimeField(verbose_name=b'date record was last modified')),
            ],
        ),
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('purchased_from', models.CharField(max_length=255)),
                ('manufacturer', models.CharField(max_length=255)),
                ('active', models.BooleanField()),
                ('create_date', models.DateTimeField(verbose_name=b'date record was created')),
                ('modified_date', models.DateTimeField(verbose_name=b'date record was last modified')),
                ('location_id', models.ForeignKey(to='iotdata.Locations')),
            ],
        ),
        migrations.AddField(
            model_name='readings',
            name='reading_type_id',
            field=models.ForeignKey(to='iotdata.ReadingType'),
        ),
        migrations.AddField(
            model_name='readings',
            name='sensor_id',
            field=models.ForeignKey(to='iotdata.Sensors'),
        ),
    ]
