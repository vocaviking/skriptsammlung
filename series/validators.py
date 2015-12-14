#************************************************************************************
#                                    Validators
#************************************************************************************
#====================================================================================
#                                  Include stuff
#====================================================================================
from django.conf            import settings
from django.core.exceptions import ValidationError
import os, mimetypes
#====================================================================================
#                                    Actual Code
#====================================================================================
#------------------------------------------------------------------------------------
#                                     Filetype
#------------------------------------------------------------------------------------
def validate_mimetype(file):
    '''
    Checks if the given filetype is allowed within the SERIES_ALLOWED_MIMETYPES settings of your settings.py
    '''
    if settings.SERIES_ALLOWED_MIMETYPES is not None:
        mime = mimetypes.guess_type(file.name)[0]
        if mime is None:
            raise ValidationError('Could not get mimetype of {filename}!'.format(filename    = os.path.split(file.name)[1]))
        if mime not in settings.SERIES_ALLOWED_MIMETYPES:
            raise ValidationError('The {extension} filetype is not an allowed!'.format(extension = os.path.splitext(file.name)[1][1:].upper()))
#------------------------------------------------------------------------------------
#                                     Filesize
#------------------------------------------------------------------------------------
def validate_filesize(file):
    '''
    Checks if the given file is allowed within the SERIES_MAX_FILE_SIZE settings of your settings.py
    '''
    if settings.SERIES_MAX_FILE_SIZE < 0:
        raise NotImplementedError('SERIES_MAX_FILE_SIZE is negative!')
    elif settings.SERIES_MAX_FILE_SIZE > 0:
        if file.size > settings.SERIES_MAX_FILE_SIZE:
            raise ValidationError('{filename} is too big to upload!'.format(filename = os.path.split(file.name)[1]))