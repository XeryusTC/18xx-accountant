# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-30 00:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_logentry_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logentry',
            options={'ordering': ['time']},
        ),
        migrations.AddField(
            model_name='logentry',
            name='acting_company',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Company'),
        ),
        migrations.AlterField(
            model_name='game',
            name='log_cursor',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to='core.LogEntry'),
        ),
    ]
