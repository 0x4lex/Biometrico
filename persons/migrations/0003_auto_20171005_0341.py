# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20171005_0340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='personid',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]