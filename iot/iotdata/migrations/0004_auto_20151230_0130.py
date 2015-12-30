# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdata', '0003_auto_20151229_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='device_type',
        ),
        migrations.AddField(
            model_name='device',
            name='device_location',
            field=models.CharField(help_text=b'location of device', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_desc',
            field=models.TextField(help_text=b'description of device', null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_part_no',
            field=models.CharField(help_text=b'part number of device if available', max_length=50, null=True),
        ),
    ]
