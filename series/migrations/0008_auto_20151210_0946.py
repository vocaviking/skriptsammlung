# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0007_auto_20151209_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Uploader', null=True),
        ),
    ]
