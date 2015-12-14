#************************************************************************************
#                                  Search Indexes
#************************************************************************************
#====================================================================================
#                                  Include stuff
#====================================================================================
from haystack                   import indexes
from django.utils               import timezone
from django.contrib.auth        import get_user_model
User = get_user_model()
from .models                    import Upload, UserProfile, Meta
from django_comments.models import Comment
#====================================================================================
#                                    Actual Code
#====================================================================================
#------------------------------------------------------------------------------------
#                                   Comment Index
#------------------------------------------------------------------------------------
class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    #Content
    text              = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Comment
    def index_queryset(self, using=None):
        return self.get_model().objects.all()

#------------------------------------------------------------------------------------
#                                     Meta Index
#------------------------------------------------------------------------------------
class MetaIndex(indexes.SearchIndex, indexes.Indexable):
    #Content
    text              = indexes.CharField(document=True, use_template=True)
    
    #Filter
    meta_name         = indexes.CharField(model_attr='name')
    meta_description  = indexes.CharField(model_attr='description')
    meta_keywords     = indexes.CharField(model_attr='keywords')
    meta_lecture      = indexes.CharField(model_attr='lecture')
    #people
    #TODOTODOTODOTODOTODO
    meta_year         = indexes.IntegerField(model_attr='year')
    meta_semester     = indexes.IntegerField(model_attr='semester')
    meta_programme    = indexes.CharField(model_attr='programme')
    meta_area         = indexes.CharField(model_attr='area')
    
    #Autocomplete
    meta_name_auto       = indexes.EdgeNgramField(model_attr='name')
    meta_keywords_auto   = indexes.EdgeNgramField(model_attr='keywords')
    meta_lecture_auto    = indexes.EdgeNgramField(model_attr='lecture')
    meta_lecturer_auto   = indexes.EdgeNgramField(model_attr='lecturer')
    meta_programme_auto  = indexes.EdgeNgramField(model_attr='programme')
    meta_area_auto       = indexes.EdgeNgramField(model_attr='area')

    def get_model(self):
        return Meta
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
#------------------------------------------------------------------------------------
#                                 Upload Index
#------------------------------------------------------------------------------------     
class UploadIndex(indexes.SearchIndex, indexes.Indexable):
    #Content
    text        = indexes.CharField(document=True, use_template=True)
    
    #Autocomplete
    upload_author_auto = indexes.EdgeNgramField(model_attr='author')
##    upload_name_auto   = indexes.EdgeNgramField(model_attr='')
    def get_model(self):
        return Upload
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
#------------------------------------------------------------------------------------
#                                   User Index
#------------------------------------------------------------------------------------
class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text               = indexes.CharField(document=True, use_template=True)
    user_username_auto = indexes.EdgeNgramField(model_attr='get_username')
    #username    = indexes.CharField(    model_attr='username')
    #first_name  = indexes.CharField(    model_attr='first_name')
    #last_name   = indexes.CharField(    model_attr='last_name')
    is_staff           = indexes.BooleanField( model_attr='is_staff')
    #Profile informatioon
    def get_model(self):
        return User
    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.all()