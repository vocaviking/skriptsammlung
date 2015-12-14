# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meta',
            name='upload',
        ),
        migrations.AddField(
            model_name='upload',
            name='meta',
            field=models.ManyToManyField(blank=True, to='series.Meta'),
        ),
    ]
