# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 20:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0002_auto_20171218_2020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership', models.BooleanField()),
                ('age', models.IntegerField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.Car')),
            ],
        ),
        migrations.CreateModel(
            name='RentalDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.Rental')),
            ],
        ),
    ]
