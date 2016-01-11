# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 13:57
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_content_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='title'),
        ),
    ]