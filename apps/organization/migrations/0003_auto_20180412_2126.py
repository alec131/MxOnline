# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-12 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_courseorg_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseorg',
            name='category',
        ),
        migrations.AddField(
            model_name='courseorg',
            name='ct',
            field=models.CharField(choices=[('pxjg', '\u57f9\u8bad\u673a\u6784'), ('gx', '\u9ad8\u6821'), ('gr', '\u4e2a\u4eba')], default='\u57f9\u8bad\u673a\u6784', max_length=20, verbose_name='\u673a\u6784\u7c7b\u522b'),
        ),
    ]
