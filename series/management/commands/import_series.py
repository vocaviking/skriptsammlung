import os, re, mimetypes
from django.contrib.auth         import get_user_model
User = get_user_model()
from django.core.files           import File
from django.core.management.base import BaseCommand, CommandError
from django.utils                import timezone
from series.models               import Upload, Meta
from series.pdf2txt              import pdf2txt
from series.validators           import validate_mimetype

class Command(BaseCommand):
    help = 'This command is for importing the liblist data into the app-database.'
    def _file_import(self, filepath, user, meta, options, counter):
        self.stdout.write('Trying to import: {file}'.format(file=filepath))
        file = File(open(filepath,'rb'))
        try:
            validate_mimetype(file)
        except:
            self.stdout.write('Filetype not supported!')
            return
        upload              = Upload()
        upload.meta         = meta
        upload.file         = file
        upload.filename     = os.path.split(file.name)[1]
        upload.date         = timezone.now()
        upload.uploader     = user
        upload.login_only   = options['login_only']
        upload.author       = options['author'][counter%len(options['author'])]
        upload.content_type = options['content_type'][counter%len(options['content_type'])]
        upload.save()
        upload.file_content_extract()
        upload.save()
        
        self.stdout.write('Successfull!')
    def add_arguments(self, parser):
        parser.add_argument('files',           nargs='+',                      help='The files which shall be imported.')
        parser.add_argument('--user',                     default='anonymous', help='The user under which the documents are added. The default is "anonymous".')
        parser.add_argument('--series',                   default='',          help='The name of the series')
        parser.add_argument('--description',              default='')
        parser.add_argument('--keywords',                 default='')
        parser.add_argument('--lecture',                  default='')
        parser.add_argument('--lecturer',                 default='')
        parser.add_argument('--year',                     default=0)
        parser.add_argument('--semester',                 default=1)
        parser.add_argument('--programme',                default='')
        parser.add_argument('--area',                     default='')
        parser.add_argument('--login_only',               default=True)
        parser.add_argument('--author',        nargs='+', default=('',))
        parser.add_argument('--content_type',  nargs='+', default=('',))
    def handle(self, *args, **options):
        #Do we have a valid user?
        try:
            user = User.objects.get(username=options['user'])
        except User.DoesNotExist:
            raise CommandError('Cannot import files under the user "{user}", because he does not exist!'.format(user=options['user']))
        #Do all file-inputs exist?
        for file in options['files']:
            if not os.path.isfile(file) and not os.path.isdir(file):
                raise CommandError('{file} does not exist!'.format(file = file))
        #Create Meta
        meta                = Meta()
        meta.name           = options['series']
        meta.description    = options['description']
        meta.keywords       = options['keywords']
        meta.lecture        = options['lecture']
        meta.lecturer       = options['lecturer']
        meta.year           = options['year']
        meta.semester       = options['semester']
        meta.programme      = options['programme']
        meta.area           = options['area']
        meta.save()

        #Import
        counter = 0
        for file in options['files']:
            #File?
            if os.path.isfile(file):
                self._file_import(file, user, meta, options, counter)
                counter += 1
            #Directory?
            elif os.path.isdir(file):
                self.stdout.write('Walking through directory: {file}'.format(file=file))
                #Walk directory
                for root, dirs, files in os.walk(file):
                    for name in files:
                        self._file_import(os.path.join(root,name),user, meta, options, counter)
                        counter += 1
        #success!
