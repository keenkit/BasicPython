# -*- coding: utf-8 -*-

from django.db import models


class Tag(models.Model):
    """docstring for Tags"""
    tag_name = models.CharField(max_length=500, verbose_name=u'Tag Name')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'Create Datetime')

    def __unicode__(self):
        return self.tag_name


class Category(models.Model):
    """docstring for Category"""
    category_name = models.CharField(max_length=50, verbose_name=u'Category Name')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'Create Datetime')

    def __unicode__(self):
        return self.category_name


class Author(models.Model):
    """docstring for Author"""
    name = models.CharField(max_length=30, verbose_name=u'Author Name')
    email = models.EmailField(blank=True, verbose_name=u'Author Email')

    def __unicode__(self):
        return u'%s' % self.name


class Article(models.Model):
    """docstring for Article"""
    caption = models.CharField(max_length=200, verbose_name=u'Caption')
    description = models.TextField(blank=True, max_length=800, verbose_name=u'Description')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name=u'Post Datetime')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'Update Datetime')
    author = models.ForeignKey(Author, verbose_name=u'Author')
    category = models.ForeignKey(Category, blank=True, verbose_name=u'Category')
    content = models.TextField(verbose_name=u'Content')
    url = models.CharField(max_length=200, blank=True, verbose_name=u'Url')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'Tags')
    active = models.BooleanField(default=False)


class Search:
    searchCount = 0
    searchString = ''

    def __init__(self, searchCount, searchString):
        self.searchCount = searchCount
        self.searchString = searchString

