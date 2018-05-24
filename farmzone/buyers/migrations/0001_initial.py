# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-24 02:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('push_notifications', '0005_applicationid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('fcm_device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='push_notifications.GCMDevice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Buyer Devices',
                'verbose_name': 'Buyer Device',
                'db_table': 'buyer_device',
            },
        ),
    ]
