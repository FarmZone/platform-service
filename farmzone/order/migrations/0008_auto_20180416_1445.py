# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-16 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20180415_0523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED'), ('COMPLETED', 'COMPLETED'), ('CART', 'CART'), ('CANCELLED', 'CANCELLED')], default='NEW', max_length=30),
        ),
    ]
