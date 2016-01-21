#************************************************************************************
#                                      Views
#************************************************************************************
#====================================================================================
#                                  Include stuff
#====================================================================================
import mimetypes, json
from bootstrap3_datetime.widgets         import DateTimePicker
from collections                         import Counter
from django                              import forms
from django.contrib.auth                 import authenticate, login, logout, get_user_model
User = get_user_model()                  
from django.contrib.auth.decorators      import login_required
from django.core.urlresolvers            import reverse
from django.http                         import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts                    import get_object_or_404, render, redirect
from django.utils                        import timezone
from django.utils.decorators             import method_decorator
from django.views.generic.detail         import DetailView
from django.views.generic.edit           import UpdateView, CreateView, DeleteView, FormView
from django_comments.models              import Comment, ContentType
from haystack.generic_views              import SearchView
from haystack.forms                      import ModelSearchForm
from haystack.query                      import SearchQuerySet
from nocaptcha_recaptcha.fields          import NoReCaptchaField
from registration.backends.default.views import RegistrationView
from .models                             import UserProfile, Upload, Meta
from .registration_form                  import RegistrationFormUniqueEmail
#====================================================================================
#                                    Actual Code
#====================================================================================
#------------------------------------------------------------------------------------
#                                    Search Forms
#------------------------------------------------------------------------------------
class search_form(ModelSearchForm):
    user       = forms.CharField(required=False)
    start_date = forms.DateField(required=False,widget=DateTimePicker(options={'format':'DD. MMM YYYY','pickTime': False}),input_formats = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d. %b %Y', '%b %d %Y', '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y', '%d %B %Y', '%d %B, %Y'])
    end_date   = forms.DateField(required=False,widget=DateTimePicker(options={'format':'DD. MMM YYYY','pickTime': False}),input_formats = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d. %b %Y', '%b %d %Y', '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y', '%d %B %Y', '%d %B, %Y'])

    def search(self):
        #First, store the SearchQuerySet received from other processing.
        sqs = super(search_form, self).search()

        if not self.is_valid():
            return self.no_query_found()
        #If we have advanced options, but not query, do a database wide search
        if ( not self.cleaned_data['q']      ) and \
             ( self.cleaned_data['user']        or \
               self.cleaned_data['start_date']  or \
               self.cleaned_data['start_date'] ):
            sqs = SearchQuerySet().all()
        elif not self.cleaned_data['q']:
            return self.no_query_found()
        #Check to see if a user was chosen.
        if self.cleaned_data['user']:
            sqs = sqs.filter(user__contains=self.cleaned_data['user'])
        #Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(date__gte=self.cleaned_data['start_date'])
        #Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(date__lte=self.cleaned_data['end_date'])
        
        #Cleaning up Results (Get rid of doubles mainly)
        sqs2 = []
        if not self.cleaned_data['models'] or 'series.userprofile' in self.cleaned_data['models']:
            users = Counter()
            for each in sqs.models(UserProfile).values_list('user_pk'):
                if each[0] is not None:
                    users[each[0]] += 1
            for each in users:
                sqs2.append(sqs.models(UserProfile).filter(user_pk=each).latest('date'))
        if not self.cleaned_data['models'] or 'django_comments.comment' in self.cleaned_data['models']:
            comments = Counter()
            for each in sqs.models(Comment).values_list('comment_pk'):
                if each[0] is not None:
                    comments[each[0]] += 1
            for each in comments:
                sqs2.append(sqs.models(Comment).filter(comment_pk=each).latest('date'))
        if not self.cleaned_data['models'] or 'series.upload' in self.cleaned_data['models']:
            metas = Counter()
            for each in sqs.models(Upload).values_list('meta_pk'):
                if each[0] is not None:
                    metas[each[0]] += 1
            for each in metas:
                sqs2.append(sqs.models(Upload).filter(meta_pk=each).latest('date'))
        return sqs2
class search_view(SearchView):
    form_class = search_form
    template_name = 'search/search.html'
    def get_context_data(self, *args, **kwargs):
        context = super(search_view, self).get_context_data(*args, **kwargs)
        #Check if we have advanced option, and open the form container if we do
        if self.request.GET.get('user','')       != '' or \
           self.request.GET.get('start_date','') != '' or \
           self.request.GET.get('end_date','')   != '':
            context['advanced'] = True
        else:
            context['advanced'] = False
        return context
#------------------------------------------------------------------------------------
#                                    General Site
#------------------------------------------------------------------------------------
def index(request):
    context = {
                   'user_num'    : User.objects.all().count(),
                   'upload_num'  : Upload.objects.all().count(),
                   'meta_num'    : Meta.objects.all().count(),
                   'comment_num' : Comment.objects.all().count(),
              }
    return render(request, 'webpage/index.html', context)
def about(request):
    return render(request, 'webpage/about.html')
def contact(request):
    return render(request, 'webpage/contact.html')
#------------------------------------------------------------------------------------
#                                     Overviews
#------------------------------------------------------------------------------------
def semester_overview(request):
    semester_list  = [ entry['semester']  for entry in Meta.objects.all().values('semester').order_by('-semester').distinct()]
    programme_list = [ entry['programme'] for entry in Meta.objects.all().values('programme').order_by('-programme').distinct()]
    grid = {}
    for semester in semester_list:
        grid[semester]  = {}
    for semester in semester_list:
        for programme in programme_list:
            lecture_list = [ entry['lecture'] for entry in Meta.objects.filter(semester=semester).filter(programme=programme).values('lecture').order_by('-lecture').distinct()]
            if len(lecture_list)>0:
                grid[semester][programme] = lecture_list
    context = {'grid':grid}
    return render(request, 'overview/semester.html', context)
def people_overview(request):
    year_list      = [ entry['year']      for entry in Meta.objects.all().values('year').order_by('-year').distinct()]
    programme_list = [ entry['programme'] for entry in Meta.objects.all().values('programme').order_by('-programme').distinct()]
    grid = {}
    for year in year_list:
        grid[year]  = {}
    for year in year_list:
        for programme in programme_list:
            lecturer_list = [ entry['lecturer'] for entry in Meta.objects.filter(year=year).filter(programme=programme).values('lecturer').order_by('-lecturer').distinct()]
            if len(lecturer_list)>0:
                grid[year][programme] = lecturer_list
    context = {'grid':grid}
    return render(request, 'overview/people.html', context)
#------------------------------------------------------------------------------------
#                                      Series
#------------------------------------------------------------------------------------
#....................................................................................
#                                   Detail View
#....................................................................................
class upload_detail(DetailView):
    model         = Upload
    template_name = 'uploads/detail.html'
    def get_context_data(self, **kwargs):
        context = super(upload_detail, self).get_context_data(**kwargs)
        context['more_like_this']  = SearchQuerySet().more_like_this(self.get_object()).models(Upload)[:5]
        return context
class meta_detail(DetailView):
    model         = Meta
    template_name = 'metas/detail.html'
    def get_context_data(self, **kwargs):
        context = super(meta_detail, self).get_context_data(**kwargs)
        context['upload_latest']   = Upload.objects.filter(meta=self.get_object()).order_by('-date').first()
        context['upload_authors']  = [ upload['author']   for upload in Upload.objects.filter(meta=self.get_object()).order_by('author').values('author').distinct()    ]
        context['upload_uploader'] = [ User.objects.get(pk=upload['uploader']) for upload in Upload.objects.filter(meta=self.get_object()).order_by('uploader').values('uploader').distinct()]
        context['upload_list']     = Upload.objects.filter(meta=self.get_object()).order_by('-date')
        context['comment']         = Comment.objects.filter(content_type = ContentType.objects.get_for_model(Meta))
        context['more_like_this']  = SearchQuerySet().more_like_this(self.get_object()).models(Upload)[:5]
        return context
#....................................................................................
#                                   Edit View
#....................................................................................
class meta_edit(UpdateView):
    model         = Meta
    template_name = 'metas/edit.html'
    fields        = [ 'name',
                      'description',
                      'keywords',
                      'lecture',
                      'lecturer',
                      'year',
                      'semester',
                      'programme',
                      'area',
                    ]
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(meta_edit, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse('series:meta_detail', args=[self.object.id])
    def get_form(self, form_class):
        form = super(meta_edit, self).get_form(form_class)
        form.fields['captcha'] = NoReCaptchaField(help_text   = 'Commencing Turing-Test...')
        return form
#....................................................................................
#                                   Create View
#....................................................................................
class meta_create(CreateView):
    model         = Meta
    template_name = 'metas/create.html'
    fields        = [ 'name',
                      'description',
                      'keywords',
                      'lecture',
                      'lecturer',
                      'year',
                      'semester',
                      'programme',
                      'area',
                    ]
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(meta_create, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse('series:meta_detail', args=[self.object.id])
    def get_form(self, form_class):
        form = super(meta_create, self).get_form(form_class)
        form.fields['captcha'] = NoReCaptchaField(help_text   = 'Commencing Turing-Test...')
        upload_form = forms.models.modelform_factory(Upload,fields=('file','author','content_type'))
        for field in upload_form.base_fields:
            form.fields[field] = upload_form.base_fields[field]
        return form
    def form_valid(self, form):
        response            = super(meta_create, self).form_valid(form)
        meta                = form.save()
        upload              = Upload()
        upload.meta         = meta
        upload.file         = self.request.FILES['file']
        upload.filename     = self.request.FILES['file'].name
        upload.date         = timezone.now()
        upload.uploader     = self.request.user
        upload.ip           = self.request.META['REMOTE_ADDR']
        upload.login_only   = True
        upload.author       = form.cleaned_data['author']
        upload.content_type = form.cleaned_data['content_type']
        upload.file_content_extract()
        upload.save()
        return response
class upload_create(CreateView):
    model         = Upload
    template_name = 'uploads/create.html'
    fields        = [ 'file',
                      'author',
                      'content_type',
                    ]
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        try:
            self.meta = Meta.objects.get(pk=kwargs['pk'])
        except:
            self.meta = None
        if self.meta is None:
            response = HttpResponseRedirect(reverse('series:index'))
        else:
            response = super(upload_create, self).dispatch(*args, **kwargs)
        return response
    def get_form(self, form_class):
        form = super(upload_create, self).get_form(form_class)
        form.fields['captcha'] = NoReCaptchaField(help_text   = 'Commencing Turing-Test...')
        return form
    def get_success_url(self):
        return reverse('series:upload_detail', args=[self.object.id])
    def get_context_data(self, **kwargs):
        context = super(upload_create, self).get_context_data(**kwargs)
        context['meta'] = self.meta
        return context
    def form_valid(self, form):
        response            = super(upload_create, self).form_valid(form)
        upload              = form.save()
        upload.meta         = self.meta
        upload.date         = timezone.now()
        upload.uploader     = self.request.user
        upload.ip           = self.request.META['REMOTE_ADDR']
        upload.login_only   = True
        upload.file_content_extract()
        upload.save()
        return response
#....................................................................................
#                                    Delete View
#....................................................................................
class meta_delete(DeleteView):
    model = Meta
    template_name = 'metas/delete.html'
	
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(meta_delete, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse('series:index')
    def delete(self, request, *args, **kwargs):
        Comment.objects.filter(object_pk = kwargs['pk']).delete()
        return super(meta_delete, self).delete(self, request, *args, **kwargs)
class upload_delete(DeleteView):
    model = Upload
    template_name = 'uploads/delete.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(upload_delete, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse('series:index')
    def delete(self, request, *args, **kwargs):
        #Check if meta gets deleted
        return super(upload_delete, self).delete(self, request, *args, **kwargs)
#....................................................................................
#                                   Download View
#....................................................................................
# Delivers the actual file to the User.
#....................................................................................
def upload_file(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    if upload.login_only and not request.user.is_authenticated():
        #We need to login, but aren't
        response = HttpResponseRedirect('{login}?next={next}'.format(login = reverse('series:user_login'), next = reverse('series:upload_detail',args=[pk])))
    else:
        #We can download the file
        
        #Get mimetype
        mime = mimetypes.guess_type(upload.file.name)[0]
        if mime is None:
            #Error! Couldn't get Mimetype!
            response = HttpResponseServerError('Could not get the Mimetype for the requested file!')
        else:
            #Send file
            response = HttpResponse(upload.file,
                                    content_type = mime,
                                    )
            response['Content-Disposition'] = 'attachment; filename="{filename}.{filetype}"'.format(filename = str(upload.meta.name) + ' - ' + str(upload)[:-1-len(upload.get_filetype())],
                                                                                                    filetype = upload.get_filetype(),
                                                                                                    )
        upload.downloads += 1
        upload.save()
    return response
#------------------------------------------------------------------------------------
#                                       User
#------------------------------------------------------------------------------------
#....................................................................................
#                                   Detail View
#....................................................................................
class user_detail(DetailView):
    model               = User
    context_object_name = 'object'
    slug_field          = 'username'
    slug_url_kwarg      = 'username'
    template_name       = 'users/detail.html'
    def get_context_data(self, **kwargs):
        context = super(user_detail, self).get_context_data(**kwargs)
        context['upload_list']   = Upload.objects.filter(uploader=self.get_object()).order_by('-date')
        context['comment_list']  = Comment.objects.filter(user=self.get_object()).order_by('-submit_date')
        return context
#....................................................................................
#                                   Edit View
#....................................................................................
class user_edit(UpdateView):
    model         = UserProfile
    fields        = [ 'title',
                      'degree',
                      'about_me',
                      'image',
                      'website',
                      'phone',
                      'birth_date',
                      'show_age',     
                      'show_realname',
                      'show_birthday',
                    ]
    template_name = 'users/edit.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(user_edit, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse('series:user_detail', args=[self.object.user.get_username()])
    def form_valid(self, form):
        #Save Form
        response = super(user_edit, self).form_valid(form)
        #Save First and Last Name
        user            = self.object.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name  = form.cleaned_data['last_name']
        user.save()

        return response
    def get_object(self, queryset=None):
        return self.request.user.userprofile
    def get_form(self, form_class):
        form = super(user_edit, self).get_form(form_class)
        form.fields['birth_date'].widget  = DateTimePicker(options={'format':'DD. MMM YYYY','pickTime': False})
        form.fields['birth_date'].input_formats = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d. %b %Y', '%b %d %Y', '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y', '%d %B %Y', '%d %B, %Y']

        user_form = forms.models.modelform_factory(User,fields=('first_name','last_name'))
        for field in user_form.base_fields:
            form.fields[field] = user_form.base_fields[field]
            if   field == 'email':
                form.fields[field].initial = self.object.user.email
            elif field == 'first_name':
                form.fields[field].initial = self.object.user.first_name
            elif field == 'last_name':
                form.fields[field].initial = self.object.user.last_name
        return form
#....................................................................................
#                                 Create/Register View
#....................................................................................
class user_register(RegistrationView):
    def form_valid(self, request, form):
        username = form.clean_email().split('@')[0]
        if User.objects.filter(username__iexact=username):
            raise
        form.instance.username = username
        return super(user_register, self).form_valid(request, form)
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('series:index'))
        else:
            return super(user_register, self).dispatch(*args, **kwargs)
    def get_form_class(self, request):
        return RegistrationFormUniqueEmail
    def register(self, request, form):
        user         = form.save()
        profile      = UserProfile()
        profile.user = user
        profile.save()
        super(user_register, self).register(request, form)
#------------------------------------------------------------------------------------
#                               Autocomplete Queries
#------------------------------------------------------------------------------------
def auto_test(q, cat, show):
    results  = []
    for category in cat.split():
        #Do Query
        if   category == 'lecture':
            keys = [str(entry.object.meta.lecture) for entry in SearchQuerySet().autocomplete(meta_lecture_auto=q)]
        elif category == 'username':
            keys = [str(entry.object) for entry in SearchQuerySet().autocomplete(user_username_auto=q)]
            keys.extend([str(entry.object) for entry in SearchQuerySet().autocomplete(user_fullname_auto=q)])
        #TODO
        elif category == 'degree':
            keys = [str(entry.object.userprofile.degree) for entry in SearchQuerySet().autocomplete(user_degree_auto=q)]
        #TODO
        elif category == 'title':
            keys = [str(entry.object.userprofile.title) for entry in SearchQuerySet().autocomplete(user_title_auto=q)]
        elif category == 'area':
            keys = [str(entry.object.meta.area) for entry in SearchQuerySet().autocomplete(meta_area_auto=q)]
        elif category == 'programme':
            keys = [str(entry.object.meta.programme) for entry in SearchQuerySet().autocomplete(meta_programme_auto=q)]
        elif category == 'metaname':
            keys = [str(entry.object.meta) for entry in SearchQuerySet().autocomplete(meta_name_auto=q)]
        elif category == 'people':
            keys = [str(entry.object.author) for entry in SearchQuerySet().autocomplete(upload_author_auto=q)]
            keys.extend([str(entry.object.meta.lecturer) for entry in SearchQuerySet().autocomplete(meta_lecturer_auto=q)])
        elif category == 'keywords':
            query = SearchQuerySet().autocomplete(meta_keywords_auto=q)
            #Extract Keywords
            keys = []
            for entry in query:
                for keyword in entry.object.meta.keywords_as_list():
                    if q.lower() in keyword.lower():
                        keys.append(keyword)
        else:
            keys = []
        #Remove Doubles
        keys  = [entry[0] for entry in Counter(keys).most_common(5)]
        #Convert into JSON
        for entry in keys:
            json = {}
            json['label']    = entry
            if show.lower() == 'true':
                catkey = { 
                           'lecture'    : 'Lecture',
                           'username'   : 'User',
                           'metaname'   : 'Series',
                           'title'      : 'Title',
                           'degree'     : 'Degree',
                           'people'     : 'People',
                           'area'       : 'Area',
                           'programme'  : 'Graduation Course',
                           'keywords'   : '',
                         }
                json['category'] = catkey[category]
            else:
                json['category'] = ''
            results.append(json)
    #Return Results
    return results
#------------------------------------------------------------------------------------
#                               Autocomplete Views
#------------------------------------------------------------------------------------
def autocomplete(request):
    if request.is_ajax() and len(request.GET.get('q',''))>=3:
        data = json.dumps(auto_test(request.GET.get('q',''),request.GET.get('category','keywords lecture people area username metaname'),request.GET.get('show','false')))
    else:
        data = '[]'
    return HttpResponse(data, content_type='application/json')