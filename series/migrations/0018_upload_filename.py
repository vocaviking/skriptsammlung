# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0017_auto_20160119_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='filename',
            field=models.CharField(max_length=250, editable=False, default=''),
        ),
    ]
