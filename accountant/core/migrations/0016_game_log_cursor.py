# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-09 23:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_logentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='log_cursor',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.LogEntry'),
        ),
    ]
