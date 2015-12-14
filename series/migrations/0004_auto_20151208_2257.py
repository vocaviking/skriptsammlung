# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0003_auto_20151208_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meta',
            name='upload',
        ),
        migrations.AddField(
            model_name='upload',
            name='meta',
            field=models.ForeignKey(to='series.Meta', null=True),
        ),
    ]
