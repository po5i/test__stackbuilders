# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartype',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
