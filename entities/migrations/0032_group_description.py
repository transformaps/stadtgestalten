# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-20 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0031_auto_20160613_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True, default='', max_length=200, verbose_name='Kurzbeschreibung'),
        ),
    ]
