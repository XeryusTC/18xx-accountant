# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-10 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20170112_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='ipo_shares',
            field=models.IntegerField(default=None),
        ),
    ]
