# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_vote_endorse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content2.Content'),
        ),
    ]
