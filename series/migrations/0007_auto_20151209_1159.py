# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0006_meta_clicks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meta',
            name='clicks',
        ),
        migrations.AddField(
            model_name='upload',
            name='downloads',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
