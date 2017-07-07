# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0012_auto_20170619_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', through='memberships.Membership', to='gestalten.Gestalt'),
        ),
    ]
