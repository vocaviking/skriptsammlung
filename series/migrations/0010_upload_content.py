# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0009_auto_20151213_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='content',
            field=models.TextField(editable=False, default=''),
        ),
    ]
