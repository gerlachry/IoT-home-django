# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdata', '0005_auto_20160102_2055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feed',
            old_name='reading_name',
            new_name='reading_id',
        ),
        migrations.AlterField(
            model_name='feed',
            name='feed_desc',
            field=models.TextField(help_text=b'description of the feed', null=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='feed_name',
            field=models.CharField(help_text=b'unique feed name to use when sending data to the api and looking up data also used as the index name', max_length=50),
        ),
    ]
