# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-14 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='seller_code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
