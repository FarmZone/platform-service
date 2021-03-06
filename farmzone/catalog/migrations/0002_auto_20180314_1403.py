# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-14 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('sub_product_code', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('display_name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Sub Product',
                'verbose_name_plural': 'Sub products',
                'db_table': 'sub_product',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='display_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product'),
        ),
    ]
