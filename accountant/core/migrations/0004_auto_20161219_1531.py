# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='cash',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='bank_cash',
            field=models.IntegerField(default=12000),
        ),
        migrations.AddField(
            model_name='player',
            name='cash',
            field=models.IntegerField(default=0),
        ),
    ]
