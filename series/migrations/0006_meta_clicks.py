# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0005_auto_20151209_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='meta',
            name='clicks',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
