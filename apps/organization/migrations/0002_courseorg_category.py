# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-11 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('organization', '\u57f9\u8bad\u673a\u6784'), ('school', '\u9ad8\u6821'), ('personal', '\u4e2a\u4eba')], default='\u57f9\u8bad\u673a\u6784', max_length=20, verbose_name='\u673a\u6784\u7c7b\u522b'),
        ),
    ]