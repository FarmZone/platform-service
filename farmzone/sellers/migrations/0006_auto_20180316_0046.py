# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-16 00:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20180314_1435'),
        ('sellers', '0005_preferredseller'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerSubProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Seller Sub Products',
                'verbose_name': 'Seller Sub Product',
                'db_table': 'seller_sub_product',
            },
        ),
        migrations.AddField(
            model_name='seller',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sellerowner',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sellersubproduct',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Seller'),
        ),
        migrations.AddField(
            model_name='sellersubproduct',
            name='sub_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.SubProduct'),
        ),
    ]