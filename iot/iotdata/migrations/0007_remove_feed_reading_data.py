# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdata', '0006_auto_20160102_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='reading_data',
        ),
    ]
