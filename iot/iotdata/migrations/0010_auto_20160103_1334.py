# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdata', '0009_auto_20160103_0053'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_type', models.CharField(help_text=b'feed type', max_length=255)),
                ('feed_desc', models.TextField(help_text=b'feed description', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='feed',
            name='reading_type',
            field=models.ForeignKey(verbose_name=b'reading name', to='iotdata.ReadingType'),
        ),
        migrations.AddField(
            model_name='feed',
            name='feed_type',
            field=models.ForeignKey(default=1, to='iotdata.FeedType'),
            preserve_default=False,
        ),
    ]
