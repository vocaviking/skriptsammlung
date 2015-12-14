#************************************************************************************
#                                   Admin Views
#************************************************************************************
#====================================================================================
#                                  Include stuff
#====================================================================================
from django.contrib             import admin
from django.contrib.auth.admin  import UserAdmin
from django.contrib.auth        import get_user_model
User = get_user_model()
from .models                    import Upload, Meta, UserProfile
import reversion
#====================================================================================
#                                    Actual Code
#====================================================================================
#------------------------------------------------------------------------------------
#                                     Uploads
#------------------------------------------------------------------------------------
class UploadBaseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields':['file','date','uploader','ip']                       }),
        ('File Meta',        {'fields':['meta'],                       'classes':['collapse']}),
        ('File Information', {'fields':['author','content_type'],      'classes':['collapse']}),
        ('Security',         {'fields':['login_only'],                 'classes':['collapse']}),
    ]
    list_display = ('date','uploader','author','meta','content_type','login_only')
    list_filter  = ['date', 'uploader', 'content_type', 'login_only']
class UploadAdmin(reversion.VersionAdmin, UploadBaseAdmin):
    pass
admin.site.register(Upload, UploadAdmin)

#------------------------------------------------------------------------------------
#                                      Meta
#------------------------------------------------------------------------------------
class MetaBaseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                    {'fields':['name','description','keywords']                           }),
        ('Lecture Information',   {'fields':['lecture','lecturer','area','year'], 'classes':['collapse']}),
        ('Programme Information', {'fields':['semester','programme'],             'classes':['collapse']}),
    ]
    list_display = ('name','lecture','lecturer','area','year','semester','programme')
    list_filter  = ['lecture','lecturer','area','year','semester','programme']
class MetaAdmin(reversion.VersionAdmin, MetaBaseAdmin):
    pass
admin.site.register(Meta, MetaAdmin)
#------------------------------------------------------------------------------------
#                                  User Profiles
#------------------------------------------------------------------------------------
class UserProfileInline(admin.StackedInline):
    model               = UserProfile
    can_delete          = False
    verbose_name_plural = 'profile'
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
admin.site.unregister(User)
admin.site.register(User, UserAdmin)