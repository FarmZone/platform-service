# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-14 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20180314_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('key', models.CharField(blank=True, max_length=50, null=True)),
                ('value', models.CharField(blank=True, max_length=50, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product')),
            ],
            options={
                'db_table': 'product_detail',
                'verbose_name_plural': 'Product Details',
                'verbose_name': 'Product Detail',
            },
        ),
        migrations.AlterUniqueTogether(
            name='productdetail',
            unique_together=set([('product', 'key')]),
        ),
    ]
