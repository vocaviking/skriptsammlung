# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0004_auto_20151208_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='meta',
            name='area',
            field=models.CharField(max_length=50, verbose_name='Area of the Lecture', default='', help_text='(e.g. Optics)'),
        ),
        migrations.AddField(
            model_name='meta',
            name='description',
            field=models.TextField(default='', help_text='Enter a short description of the files content. This is what people will see, if not logged in.'),
        ),
        migrations.AddField(
            model_name='meta',
            name='keywords',
            field=models.TextField(default='', help_text='Enter a set of keywords describing the content. Make it short and proper!'),
        ),
        migrations.AddField(
            model_name='meta',
            name='lecturer',
            field=models.CharField(max_length=50, verbose_name='Speaker', default='', help_text='The speaker/tutor/instructor of said lecture.'),
        ),
        migrations.AddField(
            model_name='meta',
            name='programme',
            field=models.CharField(max_length=50, verbose_name='Graduation Course', default='', help_text='Graduation Course the lecture belongs to. (e.g. Bachelor of Science in Physics)'),
        ),
        migrations.AddField(
            model_name='meta',
            name='semester',
            field=models.SmallIntegerField(choices=[(1, '1. Semester'), (2, '2. Semester'), (3, '3. Semester'), (4, '4. Semester'), (5, '5. Semester'), (6, '6. Semester'), (7, '7. Semester'), (8, '8. Semester'), (9, '9. Semester'), (10, '10. Semester')], default=1, help_text='Graduate Level of the Lecture.'),
        ),
        migrations.AddField(
            model_name='meta',
            name='year',
            field=models.SmallIntegerField(default=2015),
        ),
        migrations.AddField(
            model_name='upload',
            name='author',
            field=models.CharField(max_length=50, verbose_name='Author', default='', help_text='Here belongs the author of this file. Probably you.'),
        ),
        migrations.AddField(
            model_name='upload',
            name='content_type',
            field=models.CharField(max_length=2, verbose_name='Content Type of the Upload', default='E', choices=[('Exercise', (('Ea', 'Exercise (without a Solution in it)'), ('EA', 'Exercise with Solution'))), ('Exam', (('Ta', 'Exam (without a Solution in it)'), ('TA', 'Exam with Solution'))), ('Script', (('s', 'Script approved by the Lecturer'), ('S', 'Unapproved Script'))), ('Solution', (('ea', 'Solution to an Exercise'), ('ta', 'Solution to an Exam/Test')))]),
        ),
        migrations.AddField(
            model_name='upload',
            name='ip',
            field=models.GenericIPAddressField(verbose_name='IP-address of the Uploader', default='0.0.0.0'),
        ),
        migrations.AddField(
            model_name='upload',
            name='login_only',
            field=models.BooleanField(verbose_name='Login required', default=True, help_text='Require login for downloading the file.'),
        ),
    ]
