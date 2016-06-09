# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-07 09:58
from __future__ import unicode_literals

from django.db import migrations
import entities.models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0028_attention'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=entities.models.AutoSlugField(populate_from='name', reserve=['gestalt', 'stadt'], unique=True, validators=[entities.models.validate_reservation], verbose_name='Adresse der Gruppenseite'),
        ),
    ]