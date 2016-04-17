# -*- coding: utf-8 -*-
from blog.models import Article, Tag, Author, Category, Search
from Services.models import *
from Utility.UtilityHelper import HTTPHelper, RedisHelper, RedisTimeOut
from django.db.models import Q
from django.db import connection
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


KEY_BLOGLIST = 'blog_list'
KEY_TAGS = 'tags'
KEY_CATEGORIES = 'categories'

KEY_BLOG_PREFIX = 'blog_'
KEY_BLOG_KEYWORDS_PREFIX = 'blog_keywords_'
KEY_TAG_PREFIX = 'tag_'
KEY_CAT_PREFIX = 'cat_'

KEY_SEARCH_PREFIX = 'search_'

KEY_ANNO = 'announcement'
KEY_COMMENTS = 'comments'
KEY_CATEGORIES_COUNT_BY_ARTICLE = 'cat_count_by_article'
KEY_TOP_VIEW = 'top_view'


SQL_GET_BLOGLIST = 'SELECT a.id, a.caption, a.publish_time, a.content, a.description, a.url' \
                   'FROM BasicPython.blog_article ' \
                   'WHERE a.active = true ORDER BY a.publish_time DESC;'

SQL_GET_BLOG_COMMENTS = 'SELECT a.id,COUNT(c.id) AS NumCount, e.viewCount, e.praiseCount '\
                    'FROM BasicPython.blog_article a LEFT JOIN BasicPython.Services_comment c ON a.id = c.article_id '\
                    'LEFT JOIN BasicPython.Services_evaluation e ON a.id = e.article_id '\
                    'WHERE a.active = true GROUP BY a.id'

SQL_GET_CATEGORY_COUNTS_BY_BLOG = 'SELECT c.id, c.category_name, COUNT(c.id) AS NumCount ' \
                   'FROM BasicPython.blog_article a LEFT JOIN BasicPython.blog_category c ON a.category_id = c.id ' \
                   'WHERE a.active = true GROUP BY c.id'

SQL_VIEW_TOP = 'SELECT a.id, a.caption, a.url, e.viewCount '\
                    'FROM BasicPython.blog_article a LEFT JOIN BasicPython.Services_evaluation e ON a.id = e.article_id '\
                    'WHERE a.active = true ORDER BY e.viewCount DESC LIMIT 0,10'

class BlogHelper:
    """
    Helper class for Blog view
    """

    def __init__(self):
        pass

    @staticmethod
    def get_blog_comments():
        """
        Return comments
        """
        commentsAll = RedisHelper.get_cache(KEY_COMMENTS)
        if RedisHelper.is_cache_exist(KEY_COMMENTS) is False:
            commentsAll = list(Comment.objects.raw(SQL_GET_BLOG_COMMENTS))
            RedisHelper.create_cache(KEY_COMMENTS, commentsAll, RedisTimeOut.REDIS_TIMEOUT_5_MIN)
        return commentsAll

    @staticmethod
    def get_categories_group_count():
        """
        Return categories count by article
        """
        categoriesByArticle = RedisHelper.get_cache(KEY_CATEGORIES_COUNT_BY_ARTICLE)
        if RedisHelper.is_cache_exist(KEY_CATEGORIES_COUNT_BY_ARTICLE) is False:
            categoriesByArticle = list(Comment.objects.raw(SQL_GET_CATEGORY_COUNTS_BY_BLOG))
            RedisHelper.create_cache(KEY_CATEGORIES_COUNT_BY_ARTICLE, categoriesByArticle, RedisTimeOut.REDIS_TIMEOUT_1_DAYS)
        return categoriesByArticle

    @staticmethod
    def get_top_view():
        """
        Return top articles by viewCount
        """
        topView = RedisHelper.get_cache(KEY_TOP_VIEW)
        if RedisHelper.is_cache_exist(KEY_TOP_VIEW) is False:
            topView = list(Comment.objects.raw(SQL_VIEW_TOP))
            RedisHelper.create_cache(KEY_TOP_VIEW, topView, RedisTimeOut.REDIS_TIMEOUT_5_MIN)
        return topView


    @staticmethod
    def get_id_by_url(url):
        """
        Return url by blogId
        """
        urllist = BlogHelper.get_bloglist_all()
        for el in urllist:
            if el.url == url:
                return el.id

    @staticmethod
    def get_bloglist_all():
        """
        Return all blogs
        """
        bloglist = RedisHelper.get_cache(KEY_BLOGLIST)
        if RedisHelper.is_cache_exist(KEY_BLOGLIST) is False:
            bloglist = Article.objects.filter(active=True).order_by('-publish_time')
            RedisHelper.create_cache(KEY_BLOGLIST, bloglist, RedisTimeOut.REDIS_TIMEOUT_ONE_HOUR)
        return bloglist

    @staticmethod
    def get_blog(id):
        """
        Return single blog by id
        """
        key = KEY_BLOG_PREFIX + str(id)
        blog = RedisHelper.get_cache(key)
        if RedisHelper.is_cache_exist(key) is False:
            blog = Article.objects.get(id=id, active=True)
            RedisHelper.create_cache(key, blog, RedisTimeOut.REDIS_TIMEOUT_1_DAYS)
        return blog

    @staticmethod
    def get_blog_keywords(id):
        """
        Return keywords for one blog
        """
        key = KEY_BLOG_KEYWORDS_PREFIX + str(id)
        keywords = RedisHelper.get_cache(key)
        if RedisHelper.is_cache_exist(key) is False:
            keywords = list(BlogHelper.get_blog(id).tags.all())
            RedisHelper.create_cache(key, keywords, RedisTimeOut.REDIS_TIMEOUT_1_DAYS)
        return keywords

    @staticmethod
    def get_tags_all():
        """
        Return all tags
        """
        tags = RedisHelper.get_cache(KEY_TAGS)
        if RedisHelper.is_cache_exist(KEY_TAGS) is False:
            tags = Tag.objects.all()
            RedisHelper.create_cache(KEY_TAGS, tags, RedisTimeOut.REDIS_TIMEOUT_1_DAYS)
        return tags

    @staticmethod
    def get_categories_all():
        """
        Return all categories
        """
        categories = RedisHelper.get_cache(KEY_CATEGORIES)
        if RedisHelper.is_cache_exist(KEY_CATEGORIES) is False:
            categories = Category.objects.all()
            RedisHelper.create_cache(KEY_CATEGORIES, categories, RedisTimeOut.REDIS_TIMEOUT_1_DAYS)
        return categories

    @staticmethod
    def get_bloglist_by_tag(tag):
        """
        Return blog list filter by tag
        """
        key = KEY_TAG_PREFIX + str(tag.id)
        blogs = RedisHelper.get_cache(key)
        if RedisHelper.is_cache_exist(key) is False:
            blogs = tag.article_set.filter(active=True).order_by('-publish_time')
            RedisHelper.create_cache(key, blogs, RedisTimeOut.REDIS_TIMEOUT_1_DAYS)
        return blogs

    @staticmethod
    def get_bloglist_by_category(cat):
        """
        Return blog list filter by category
        """
        key = KEY_CAT_PREFIX + str(cat.id)
        blogs = RedisHelper.get_cache(key)
        if RedisHelper.is_cache_exist(key) is False:
            blogs = Article.objects.filter(category=cat, active=True).order_by('-publish_time')
            RedisHelper.create_cache(key, blogs, RedisTimeOut.REDIS_TIMEOUT_1_DAYS)
        return blogs

    @staticmethod
    def get_bloglist_by_search(txtSearch):
        """
        Return blog list filter by search keyword
        """
        key = KEY_SEARCH_PREFIX + txtSearch.upper()
        blogs = RedisHelper.get_cache(key)
        if RedisHelper.is_cache_exist(key) is False:
            blogs = Article.objects.filter(Q(caption__icontains=txtSearch) | Q(content__icontains=txtSearch)
                                           , active=True).order_by('-publish_time')
            RedisHelper.create_cache(key, blogs, RedisTimeOut.REDIS_TIMEOUT_1_DAYS)
            #print connection.queries
        return blogs

    @staticmethod
    def clear_caches(*args):
        """
        Clear all caches
        """
        RedisHelper.clear_all_cache(*args)

    @staticmethod
    def get_announcement():
        """
        Return announcement
        """
        return RedisHelper.get_cache(KEY_ANNO)

    @staticmethod
    def set_announcement(arg):
        if RedisHelper.is_cache_exist(KEY_ANNO) is False:
            RedisHelper.create_cache(KEY_ANNO, arg, RedisTimeOut.REDIS_TIMEOUT_1_DAYS)

    @staticmethod
    def send_comment_mail(article_id, userName, messageContent, ip, userContact):
        # send_mail(subject, content, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=True)
        blog = BlogHelper.get_blog(article_id)
        text_content = 'test'
        html_content = u'<p><font color=\'blue\'>ARTICLE: </font>{0}</p> ' \
                       u'<p><font color=\'blue\'>USERNAME: </font>{1}</p> ' \
                       u'<p><font color=\'blue\'>USERCONTACT: </font>{2}</p>' \
                       u'<p><font color=\'blue\'>IP: </font>{3}</p> ' \
                       u'<p><font color=\'blue\'>CONTENT:</font><p><b>{4}</b></p></p>'\
                       u'<p><font color=\'blue\'>LINK:</font><p><b>' \
                       u'<a href=\'{5}\' target=\'_blank\'>{5}</a></b></p></p>'.format(blog.caption,
                             userName, userContact, ip, messageContent, settings.BLOG_ROOT_URL+blog.url)
        BlogHelper.sendmail("New Comment From BasicPython!", text_content, html_content)

    @staticmethod
    def send_praise_mail(article_id):
        blog = BlogHelper.get_blog(article_id)
        text_content = 'test'
        html_content = u'<p><font color=\'blue\'>ARTICLE: </font><b>{0}</b><font color=\'blue\'> got a LIKE!</font></p> ' \
                       u'<p><font color=\'blue\'>LINK:</font><p><b>' \
                       u'<a href=\'{1}\' target=\'_blank\'>{1}</a></b></p></p>'.\
                            format(blog.caption, settings.BLOG_ROOT_URL+blog.url)
        BlogHelper.sendmail("New Like from BasicPython", text_content, html_content)

    @staticmethod
    def sendmail(subject, text_content, html_content):
        from_email, to = settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()