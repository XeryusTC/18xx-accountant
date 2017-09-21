# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20170921_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='receiving_company',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Company'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='receiving_player',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Player'),
        ),
    ]