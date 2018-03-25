# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-22 09:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sellers', '0009_auto_20180322_0949'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='preferredseller',
            unique_together=set([('seller', 'user')]),
        ),
    ]
