# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-05 07:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('desc', models.CharField(blank=True, max_length=1024, null=True)),
                ('solution', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('desc', models.CharField(blank=True, max_length=1024, null=True)),
                ('solution', models.CharField(blank=True, max_length=1024, null=True)),
                ('challenges', models.ManyToManyField(related_name='games', to='game.Challenge')),
            ],
        ),
    ]
