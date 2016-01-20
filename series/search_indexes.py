#************************************************************************************
#                                  Search Indexes
#************************************************************************************
#====================================================================================
#                                  Include stuff
#====================================================================================
from django_comments.models import Comment
from django.utils           import timezone
from haystack               import indexes
from .models                import Upload, UserProfile, Meta
#====================================================================================
#                                    Actual Code
#====================================================================================
#------------------------------------------------------------------------------------
#                                   Comment Index
#------------------------------------------------------------------------------------
class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    #Content
    text       = indexes.CharField(document=True, use_template=True)
    #Filter    
    date       = indexes.DateField(model_attr='submit_date')
    user       = indexes.CharField(model_attr='user__get_username')
    comment_pk = indexes.IntegerField(model_attr='pk')
    #Pre-Rendering
    rendered   = indexes.CharField(use_template=True,indexed=False)
    #Functions
    def get_model(self):
        return Comment
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
#------------------------------------------------------------------------------------
#                                 Upload Index
#------------------------------------------------------------------------------------     
class UploadIndex(indexes.SearchIndex, indexes.Indexable):
    #Content
    text                = indexes.CharField(document=True, use_template=True)
    #Filter
    date                = indexes.DateField(model_attr='date')
    user                = indexes.CharField(model_attr='uploader__get_username')
    meta_pk             = indexes.IntegerField(model_attr='meta__pk')
    #Autocomplete Upload
    upload_author_auto  = indexes.EdgeNgramField(model_attr='author')
    #Autocomplete Meta
    meta_name_auto      = indexes.EdgeNgramField(model_attr='meta__name')
    meta_keywords_auto  = indexes.EdgeNgramField(model_attr='meta__keywords')
    meta_lecture_auto   = indexes.EdgeNgramField(model_attr='meta__lecture')
    meta_lecturer_auto  = indexes.EdgeNgramField(model_attr='meta__lecturer')
    meta_programme_auto = indexes.EdgeNgramField(model_attr='meta__programme')
    meta_area_auto      = indexes.EdgeNgramField(model_attr='meta__area')
    #Pre-Rendering
    rendered            = indexes.CharField(use_template=True,indexed=False)
    #Functions
    def get_model(self):
        return Upload
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
#------------------------------------------------------------------------------------
#                                   User Index
#------------------------------------------------------------------------------------
class UserProfileIndex(indexes.SearchIndex, indexes.Indexable):
    #Content
    text               = indexes.CharField(document=True, use_template=True)
    #Filter
    date               = indexes.DateField(model_attr='get_birth_date')
    user               = indexes.CharField(model_attr='user__get_username')
    user_pk            = indexes.IntegerField(model_attr='user__pk')
    #Autocomplete
    user_username_auto = indexes.EdgeNgramField(model_attr='user__get_username')
    user_fullname_auto = indexes.EdgeNgramField(model_attr='user__get_full_name')
    user_degree_auto   = indexes.EdgeNgramField(model_attr='degree')
    user_title_auto    = indexes.EdgeNgramField(model_attr='title')
    #Pre-Rendering
    rendered           = indexes.CharField(use_template=True,indexed=False)
    #Functions
    def get_model(self):
        return UserProfile
    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.all()