# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-30 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_auto_20180330_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='status',
            field=models.CharField(blank=True, choices=[('NEW', 'New'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('COMPLETED', 'Resolved')], default='New', max_length=30, null=True),
        ),
    ]
