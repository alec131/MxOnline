# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-18 20:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20180418_2027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='teacher_tee',
            new_name='teacher_tell',
        ),
    ]