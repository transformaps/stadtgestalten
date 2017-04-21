# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-03-30 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('associations', '0002_auto_20170224_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='pinned',
            field=models.BooleanField(default=False, help_text='Angeheftete Beiträge werden auf der Gruppenseite zuerst angezeigt. Sie können beispielsweise für allgemeine Einleitungs- und Beschreibungstexte verwendet werden.', verbose_name='Im Intro der Gruppe anheften'),
        ),
        migrations.AlterField(
            model_name='association',
            name='public',
            field=models.BooleanField(default=False, help_text='Öffentliche Beiträge sind auch für Besucherinnen sichtbar, die nicht Mitglied der Gruppe sind', verbose_name='Öffentlich'),
        ),
        migrations.AlterField(
            model_name='association',
            name='slug',
            field=models.SlugField(default=None, help_text='Der Kurzname wird beispielsweise in der Webadresse des Beitrags verwendet.', null=True, verbose_name='Kurzname'),
        ),
    ]