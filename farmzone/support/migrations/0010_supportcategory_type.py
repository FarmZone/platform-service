# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-06 05:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0009_auto_20180503_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportcategory',
            name='type',
            field=models.CharField(choices=[('ORDER', 'ORDER'), ('QUERY', 'QUERY')], default='QUERY', max_length=30),
        ),
    ]