#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
    url(r'^bloglist/$',             'blog_list',                name='blog_list'),
    url(r'^search/$',               'blog_search',              name='blog_search'),
    url(r'^(?P<url>[^/]+)/$',          'blog_show',                name='blog_show'),
    url(r'^tag/(?P<tagname>[^/]+)/$',      'blog_filter_tag',          name='blog_filter_tag'),
    url(r'^category/(?P<categoryname>[^/]+)/$', 'blog_filter_category',     name='blog_filter_category'),
)