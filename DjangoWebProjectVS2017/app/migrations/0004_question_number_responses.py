# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-05-08 09:02
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_question_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='number_responses',
            field=models.IntegerField(default=2, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(2)]),
        ),
    ]
