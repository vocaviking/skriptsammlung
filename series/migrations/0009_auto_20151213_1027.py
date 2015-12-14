# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import series.validators


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0008_auto_20151210_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='file',
            field=models.FileField(verbose_name='File Selection', upload_to='series', validators=[series.validators.validate_filesize, series.validators.validate_mimetype], help_text='Only PDF, TXT, and TEX files smaller than 5MB.'),
        ),
    ]
