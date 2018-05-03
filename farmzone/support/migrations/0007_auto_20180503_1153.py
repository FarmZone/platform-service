# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-03 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0012_preferredseller_is_primary'),
        ('support', '0006_auto_20180405_0303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='support',
            name='seller',
        ),
        migrations.AddField(
            model_name='support',
            name='seller_sub_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sellers.SellerSubProduct'),
        ),
    ]
