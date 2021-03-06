# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-30 05:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('seller_code', models.CharField(blank=True, max_length=20, null=True)),
                ('comment', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Support',
                'db_table': 'support',
                'verbose_name_plural': 'Supports',
            },
        ),
        migrations.CreateModel(
            name='SupportCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('category_code', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Support Category',
                'db_table': 'support_category',
                'verbose_name_plural': 'Support Categories',
            },
        ),
        migrations.AddField(
            model_name='support',
            name='support_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.SupportCategory'),
        ),
        migrations.AddField(
            model_name='support',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
