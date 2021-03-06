# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestalten', '0008_auto_20170704_1729'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('subscriptions', '0012_remove_subscription_unsubscribe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='object_id',
            new_name='subscribed_to_id',
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='content_type',
            new_name='subscribed_to_type',
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=set([('subscribed_to_type', 'subscribed_to_id', 'subscriber')]),
        ),
    ]
