# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdata', '0007_remove_feed_reading_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feed',
            old_name='reading_id',
            new_name='reading_type_id',
        ),
    ]
