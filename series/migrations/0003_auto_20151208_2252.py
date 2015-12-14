# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0002_auto_20151208_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='meta',
        ),
        migrations.AddField(
            model_name='meta',
            name='upload',
            field=models.ManyToManyField(to='series.Upload', blank=True),
        ),
    ]
