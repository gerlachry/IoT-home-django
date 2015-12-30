# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_name', models.CharField(help_text=b'unique device id to use when sending data to the api and looking up data also used as the index name', max_length=50)),
                ('device_desc', models.TextField(help_text=b'description of device')),
                ('device_part_no', models.CharField(help_text=b'part number of device if available', max_length=50)),
                ('device_type', models.CharField(help_text=b'type of sensor, temperature, humidity etc..', max_length=100)),
            ],
        ),
    ]
