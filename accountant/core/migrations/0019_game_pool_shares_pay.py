# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-28 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20170730_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='pool_shares_pay',
            field=models.BooleanField(default=False),
        ),
    ]
