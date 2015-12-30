# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdata', '0002_auto_20151229_2345'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sensor',
            new_name='Device',
        ),
    ]
