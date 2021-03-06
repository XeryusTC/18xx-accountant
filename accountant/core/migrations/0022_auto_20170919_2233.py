# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_game_treasury_shares_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='acting_player',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Player'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='action',
            field=models.IntegerField(blank=True, choices=[(0, 'Player transfers money to bank')], default=None, null=True),
        ),
        migrations.AddField(
            model_name='logentry',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
