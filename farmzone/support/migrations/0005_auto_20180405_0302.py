# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-05 03:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_auto_20180330_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED'), ('COMPLETED', 'COMPLETED')], default='NEW', max_length=30),
        ),
    ]