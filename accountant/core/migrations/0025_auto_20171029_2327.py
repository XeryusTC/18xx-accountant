# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-29 23:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20170921_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='buyer',
            field=models.CharField(default='', max_length=8),
        ),
        migrations.AddField(
            model_name='logentry',
            name='company_buyer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Company'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='company_source',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Company'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='player_buyer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Player'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='player_source',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Player'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logentry',
            name='shares',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logentry',
            name='source',
            field=models.CharField(default='', max_length=8),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='action',
            field=models.IntegerField(blank=True, choices=[(0, 'Money transfer'), (1, 'Buy/sell share')], default=None, null=True),
        ),
    ]
