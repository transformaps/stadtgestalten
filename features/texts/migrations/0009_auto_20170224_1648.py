# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 15:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0008_auto_20170224_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorship',
            name='text',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorships', to='texts.Text'),
        ),
    ]
