# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20170919_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='action',
            field=models.IntegerField(blank=True, choices=[(0, 'Money transfer')], default=None, null=True),
        ),
    ]