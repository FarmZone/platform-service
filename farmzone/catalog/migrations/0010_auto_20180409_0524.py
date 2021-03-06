# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-09 05:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20180327_0539'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubProductDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('key', models.CharField(blank=True, max_length=50, null=True)),
                ('value', models.CharField(max_length=50)),
                ('sub_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.SubProduct')),
            ],
            options={
                'db_table': 'sub_product_detail',
                'verbose_name': 'Sub Product Detail',
                'verbose_name_plural': 'Sub Product Details',
            },
        ),
        migrations.AlterUniqueTogether(
            name='subproductdetail',
            unique_together=set([('sub_product', 'key')]),
        ),
    ]
