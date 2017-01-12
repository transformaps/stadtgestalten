# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-12 07:47
from __future__ import unicode_literals

from django import db
from django.db import migrations


def copy_gestalten(apps, schema_editor):
    Gestalt1 = apps.get_model('entities.Gestalt')
    Gestalt2 = apps.get_model('gestalten.Gestalt')
    for g in Gestalt1.objects.order_by('id'):
        g2 = Gestalt2.objects.create(
                id=g.id,
                about=g.about,
                avatar=g.avatar,
                avatar_color=g.avatar_color,
                background=g.background,
                public=g.public,
                user=g.user)
    if Gestalt1.objects.all():
        max_id = Gestalt1.objects.order_by('id').last().id
        id = Gestalt1.objects.first().id
        while id <= max_id:
            try:
                g = Gestalt2.objects.create()
                id = g.id
                g.delete()
            except db.IntegrityError:
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0048_auto_20170112_0931'),
        ('gestalten', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_gestalten),
    ]