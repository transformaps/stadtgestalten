# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 07:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributions', '0004_auto_20170428_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replykey',
            name='contribution',
        ),
        migrations.RemoveField(
            model_name='replykey',
            name='gestalt',
        ),
        migrations.DeleteModel(
            name='ReplyKey',
        ),
    ]
