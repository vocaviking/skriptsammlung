from django.conf.urls import url
from . import views

urlpatterns = [
    #Search Test
    url(r'^search/$',                                       views.search_view.as_view(),   name='search'),
    #General Site
    url(r'^$',                                              views.index,                   name='index'),
    url(r'^about/$',                                        views.about,                   name='about'),
    url(r'^contact/$',                                      views.contact,                 name='contact'),
    #Indexes/Overviews
    url(r'^lectures/$',                                     views.semester_overview,       name='semester_overview'),
    url(r'^speakers/$',                                     views.people_overview,         name='people_overview'),
    #Autocomplete                                                                          
    url(r'^autocomplete/$',                                 views.autocomplete,            name='autocomplete'),
    #Series                                                                                
    url(r'^series/(?P<pk>[0-9]+)/$',                        views.meta_detail.as_view(),   name='meta_detail'),
    url(r'^files/upload/$',                                 views.meta_create.as_view(),   name='meta_create'),
    url(r'^series/(?P<pk>[0-9]+)/edit$',                    views.meta_edit.as_view(),     name='meta_edit'),
    url(r'^series/(?P<pk>[0-9]+)/delete$',                  views.meta_delete.as_view(),   name='meta_delete'),
    #Files                                                                                 
    url(r'^file/(?P<pk>[0-9]+)/$',                          views.upload_detail.as_view(), name='upload_detail'),
    url(r'^series/(?P<pk>[0-9]+)/upload$',                  views.upload_create.as_view(), name='upload_create'),
    url(r'^files/(?P<pk>[0-9]+)/download$',                 views.upload_file,             name='upload_file'),
    url(r'^files/(?P<pk>[0-9]+)/delete$',                   views.upload_delete.as_view(), name='upload_delete'),
    #User                                                                                  
    url(r'^users/profile/(?P<username>[0-9a-zA-Z._\-]+)/$', views.user_detail.as_view(),   name='user_detail'),
    url(r'^users/profile/edit$',                            views.user_edit.as_view(),     name='user_edit'),
    url(r'^users/register/$',                               views.user_register.as_view(), name='registration_register'),
]