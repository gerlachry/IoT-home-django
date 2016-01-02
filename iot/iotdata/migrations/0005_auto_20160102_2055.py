# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdata', '0004_auto_20151230_0130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_name', models.CharField(help_text=b'unique device id to use when sending data to the api and looking up data also used as the index name', max_length=50)),
                ('feed_desc', models.TextField(help_text=b'description of device', null=True)),
                ('reading_data', models.TextField(help_text=b'the value/data of the reading')),
                ('data_location', models.CharField(help_text=b'location info from where the data value originated from', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReadingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reading_name', models.CharField(help_text=b'the name of the reading, ie. temperature, humidity, switch', max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Device',
        ),
        migrations.AddField(
            model_name='feed',
            name='reading_name',
            field=models.ForeignKey(to='iotdata.ReadingType'),
        ),
    ]
