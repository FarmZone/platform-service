# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-06 08:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0012_preferredseller_is_primary'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('product_name', models.CharField(max_length=100)),
                ('product_serial_no', models.CharField(max_length=100, unique=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Seller')),
            ],
            options={
                'verbose_name_plural': 'User Products',
                'verbose_name': 'User Product',
                'db_table': 'user_product',
            },
        ),
    ]
