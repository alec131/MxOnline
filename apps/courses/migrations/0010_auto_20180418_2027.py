# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-18 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher_tee',
            field=models.CharField(default='', max_length=300, verbose_name='\u8001\u5e08\u544a\u8bc9\u4f60\u80fd\u5b66\u5230\u4ec0\u4e48'),
        ),
        migrations.AddField(
            model_name='course',
            name='youneed_know',
            field=models.CharField(default='', max_length=300, verbose_name='\u8bfe\u7a0b\u987b\u77e5'),
        ),
    ]
