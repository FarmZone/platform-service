# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-30 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20180330_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('NEW', 'New'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('COMPLETED', 'COMPLETED')], default='New', max_length=30),
        ),
    ]
