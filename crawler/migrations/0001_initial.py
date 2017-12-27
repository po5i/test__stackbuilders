# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-26 21:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crawl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('order', models.IntegerField()),
                ('comments', models.IntegerField()),
                ('points', models.IntegerField()),
                ('crawl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='crawler.Crawl')),
            ],
        ),
    ]