from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'blog.views.blog_list', name='blog_list'),
    url(r'^blog/', include('blog.urls')),

    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'service/', include('Services.urls')),
    url(r'^uploader/', include('uploader.urls')),
    url(r'about/', 'blog.views.page_about', name='about'),

    #url(r'^404/', 'blog.views.page_not_found', name='page_not_found'),
    #url(r'^500/', 'blog.views.page_error', name='page_error'),

)# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'blog.views.page_not_found'
handler500 = 'blog.views.page_error'


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )