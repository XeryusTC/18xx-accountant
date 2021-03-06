# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_logentry_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='mode',
            field=models.IntegerField(blank=True, choices=[(0, 'Pay full dividends'), (1, 'Pay half dividends'), (2, 'Withhold dividends')], default=None, null=True),
        ),
        migrations.AddField(
            model_name='logentry',
            name='revenue',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='action',
            field=models.IntegerField(blank=True, choices=[(0, 'Money transfer'), (1, 'Buy/sell share'), (2, 'Company operates')], default=None, null=True),
        ),
    ]
