# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0014_auto_20160113_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(help_text='Your Birthdate will only be shown to other Users with your permission.', verbose_name='Birthdate', default=datetime.datetime(1, 1, 1, 0, 0)),
        ),
    ]
