# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-05 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='desc',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='solution',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='desc',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='solution',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
    ]
