# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0013_userprofile_degree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meta',
            name='year',
            field=models.SmallIntegerField(default=2016),
        ),
        migrations.AlterField(
            model_name='upload',
            name='downloads',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
