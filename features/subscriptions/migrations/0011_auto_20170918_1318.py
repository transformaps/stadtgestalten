# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 11:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_auto_20170428_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filter',
            name='subscription',
        ),
        migrations.DeleteModel(
            name='SubOrUnsubscription',
        ),
        migrations.DeleteModel(
            name='Unsubscription',
        ),
        migrations.DeleteModel(
            name='Filter',
        ),
    ]
