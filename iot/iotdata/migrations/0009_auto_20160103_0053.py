# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdata', '0008_auto_20160102_2121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feed',
            old_name='reading_type_id',
            new_name='reading_type',
        ),
    ]
