#************************************************************************************
#                                     Models
#************************************************************************************
#====================================================================================
#                                  Include stuff
#====================================================================================
import datetime, os, re, mimetypes
from django.conf                import settings
from django.contrib.auth.models import User
from django.db                  import models
from django.templatetags.static import static
from django.utils               import timezone
from reversion                  import revisions as reversion
from series.pdf2txt             import pdf2txt
from .validators                import validate_mimetype, validate_filesize
#====================================================================================
#                                    Actual Code
#====================================================================================
#------------------------------------------------------------------------------------
#                                     Uploads
#------------------------------------------------------------------------------------
@reversion.register #Save History
class Upload(models.Model):
    #Meta
    meta         = models.ForeignKey('Meta',null=True)
    #The File
    file         = models.FileField(validators   = [validate_filesize, validate_mimetype],
                                    upload_to    = 'series',
                                    verbose_name = 'File Selection',
                                    help_text    = 'Only PDF, TXT, and TEX files smaller than 5MB.',
                                    )
    #Upload date
    date         = models.DateTimeField(verbose_name = 'Upload Date',
                                        default      = timezone.now,
                                        )
    #Uploader
    uploader     = models.ForeignKey(User,
                                     verbose_name = 'Uploader',
                                     null = True,
                                    )
    #Show only for logged in users?
    login_only   = models.BooleanField(default      = True,
                                       verbose_name = 'Login required',
                                       help_text    = 'Require login for downloading the file.',
                                       )
    #Author of the document
    author   = models.CharField(max_length   = 50,
                                default      = '',
                                verbose_name = 'Author',
                                help_text    = 'Here belongs the author of this file. Probably you.',
                                )
    #Type of the document
    CONTENT_TYPE_CHOICES = ( ('Exercise', (
                                              ('Ea', 'Exercise (without a Solution in it)'),
                                              ('EA', 'Exercise with Solution'),
                                          )
                             ),
                             ('Exam',     (
                                              ('Ta', 'Exam (without a Solution in it)'),
                                              ('TA', 'Exam with Solution'),
                                          )
                             ),
                             ('Script',   (
                                              ('s', 'Script approved by the Lecturer'),
                                              ('S', 'Unapproved Script'),
                                          )
                             ),
                             ('Solution', (
                                              ('ea', 'Solution to an Exercise'),
                                              ('ta', 'Solution to an Exam/Test'),
                                          )
                             ),
                           )
    content_type = models.CharField(max_length = 2,
                                    choices    = CONTENT_TYPE_CHOICES,
                                    default    = 'E',
                                    verbose_name = 'Content Type of the Upload',
                                    )
    #Downloads
    downloads       = models.PositiveIntegerField(default = 0,editable    = False)
    #Content Extract
    content         = models.TextField(default = '',editable    = False)
    #More Meta-Information is saved and connected with the Meta Model
    def file_content_extract(self):
        #Get Filetype
        mime = mimetypes.guess_type(self.file.name)[0]
        #Extract Data
        if   mime == 'application/pdf':
            try:
                content = pdf2txt(self.file.file).read()
            except:
                content = ''
        elif mime == 'text/plain' or mime == 'application/x-tex':
            self.file.open()
            content = self.file.read().decode('utf-8')
        else:
            #Don't know how to extract!!
            return
        #Cleanup Data
        content = re.sub('[\W_]',' ',content)
        content = re.sub('[\s]+',' ',content)
        #Save Extract
        self.content = content
#    def save(self, *args, **kwargs):
#        self.file_content_extract()
#        super(Upload, self).save(*args, **kwargs)
    def __str__(self):
        return str(os.path.split(self.file.file.name)[1])
    def get_filetype(self):
        return os.path.splitext(self.file.path)[1][1:].upper()
    def get_filesize(self):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        back = '0 B'
        nbytes = self.file.size*1.
        if nbytes > 0.:
            i = 0
            while nbytes >= 1024. and i < len(suffixes)-1:
                nbytes /= 1024.
                i += 1
            back = '{size:.2f} {suffix}'.format(size = nbytes, suffix = suffixes[i])
        return back
#------------------------------------------------------------------------------------
#                                    Meta Data
#------------------------------------------------------------------------------------
#This class is for saving all Meta Data, which has to be put in by the User.
#------------------------------------------------------------------------------------
@reversion.register #Save History
class Meta(models.Model):
    #Name of the File
    name         = models.CharField(max_length = 50,
                                    default    = '',
                                    help_text  = 'Enter a meaningful name, to make this file easier to find.',
                                    )
    #Description
    description  = models.TextField(default   = '',
                                    help_text = 'Enter a short description of the files content. This is what people will see, if not logged in.',
                                    )
    #Keywords
    keywords     = models.TextField(default   = '',
                                    help_text = 'Enter a set of keywords describing the content. Make it short and proper!',
                                    )
    #Title of the lecture
    lecture      = models.CharField(max_length   = 50,
                                    default      = '',
                                    verbose_name = 'Lecture',
                                    help_text    = 'Enter the lecture which this file belongs to.',
                                    )
    #Lecturer/Speaker/Tutor/Professor
    lecturer     = models.CharField(max_length   = 50,
                                    default      = '',
                                    verbose_name = 'Speaker',
                                    help_text    = 'The speaker/tutor/instructor of said lecture.',
                                    )
    #Year of the Lecture
    year            = models.SmallIntegerField(default = datetime.datetime.now().year)
    #Semester in which the lecture belongs
    SEMESTER_CHOICES = ( ( 1, '1. Semester'),
                         ( 2, '2. Semester'),
                         ( 3, '3. Semester'),
                         ( 4, '4. Semester'),
                         ( 5, '5. Semester'),
                         ( 6, '6. Semester'),
                         ( 7, '7. Semester'),
                         ( 8, '8. Semester'),
                         ( 9, '9. Semester'),
                         ( 10, '10. Semester'),)
    semester = models.SmallIntegerField(choices   = SEMESTER_CHOICES,
                                        default   = 1,
                                        help_text = 'Graduate Level of the Lecture.',
                                        )
    #Programme the lecture belongs to
    programme = models.CharField(max_length   = 50,
                                 default      = '',
                                 verbose_name = 'Graduation Course',
                                 help_text    = 'Graduation Course the lecture belongs to. (e.g. Bachelor of Science in Physics)',
                                 )
    #Area of Physics
    area         = models.CharField(max_length   = 50,
                                    default      = '',
                                    verbose_name = 'Area of the Lecture',
                                    help_text    = '(e.g. Optics)'
                                    )
    def clean_keywords(self):
        self.keywords = re.sub('[\W_]',' ',self.keywords)
        self.keywords = re.sub('[\s]+',' ',self.keywords)
    def save(self, *args, **kwargs):
        self.clean_keywords()
        super(Meta, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    def keywords_as_list(self):
        return self.keywords.split()
    def get_latest_upload(self):
        return Upload.objects.filter(meta=self).order_by('-date').first()
#------------------------------------------------------------------------------------
#                                   User Profiles
#------------------------------------------------------------------------------------
@reversion.register #Save History
class UserProfile(models.Model):
    #User this Profile belongs to
    user       = models.OneToOneField(User,
                                      primary_key = True,
                                      editable    = False,
                                      )
    #Title (like Dr., Prof., Sir, ...)
    title         = models.CharField(verbose_name = 'Title',
                                     help_text    = 'e.g. Dr., Prof., Sir',
                                     default      = '',
                                     blank        = True,
                                     max_length   = 50,
                                    )
    #Degree (like PhD, B.Sc., M.Sc., ...)
    degree        = models.CharField(verbose_name = 'Degree',
                                     help_text    = 'e.g. PhD, B.Sc., M.Sc.',
                                     default      = '',
                                     blank        = True,
                                     max_length   = 50,
                                    )
    #Description
    about_me      = models.TextField(verbose_name = 'About Me',
                                     help_text    = 'Tell other Users who you are, and what you do.',
                                     default      = '',
                                     blank        = True,
                                     )
    #Personal Image                                                      
    image         = models.ImageField(verbose_name = 'Profile Image',
                                      blank        = True,
                                      null         = True,
                                      upload_to    = 'user_images',
                                      )
    #Personal Website                                                    
    website       = models.URLField(verbose_name = 'Personal Website',
                                    default      = '',
                                    blank        = True,
                                    )
    #Phone Number                                                        
    phone         = models.CharField(verbose_name = 'Phone Number',
                                     default      = '',
                                     blank        = True,
                                     max_length   = 50,
                                    )
    #Birthdate
    birth_date    = models.DateField(verbose_name = 'Birthdate',
                                     help_text    = 'Your Birthdate will only be shown to other Users with your permission.',
                                     default      = datetime.datetime(1,1,1),
                                     blank        = False,
                                    )
    #Permissions
    show_age      = models.BooleanField(verbose_name = 'Show Age',
                                        help_text    = 'Show other Users how old you are.',
                                        default      = False,
                                        blank        = False,
                                        )
    show_birthday = models.BooleanField(verbose_name = 'Show Birthday',
                                        help_text    = 'Show other Users the Day and Month of your Birthday.',
                                        default      = False,
                                        blank        = False,
                                        )
    show_realname = models.BooleanField(verbose_name = 'Show Realname',
                                        help_text    = 'Show other Users your First and Last Name.',
                                        default      = False,
                                        blank        = False,
                                        )
    def get_age(self):
        today = datetime.date.today()
        try: 
            birthday = self.birth_date.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.birth_date.replace(year=today.year, day=self.birth_date.day-1)
        if birthday > today:
            return today.year - self.birth_date.year - 1
        else:
            return today.year - self.birth_date.year
    def get_birth_date(self):
        if self.show_age and self.show_birthday:
            birth_date = self.birth_date
        elif self.show_birthday:
            birth_date = datetime.datetime(1,self.birth_date.month,self.birth_date.day)
        elif self.show_age:
            birth_date = datetime.datetime(self.birth_date.year,1,1)
        else:
            birth_date = datetime.datetime(1,1,1)
        return birth_date
    def get_image_url(self):
        if self.user.is_active:
            if self.image and hasattr(self.image, 'url'):
                img_url = self.image.url
            else:
                img_url = static('series/anonymous_user.png')
        else:
            img_url = static('series/deleted_user.png')
        return img_url
    def __str__(self):
        return self.user.get_username()
