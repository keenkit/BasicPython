# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from blog.models import Article, Tag, Author, Category, Search
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Utility.PaginatorExt import PaginatorExt
from django.views.decorators.csrf import requires_csrf_token
from Utility.UtilityHelper import HTTPHelper


from blogHelper import BlogHelper


def blog_list(request):
    """
    return blog list
    """
    bloglist = BlogHelper.get_bloglist_all()
    tags = BlogHelper.get_tags_all()
    categories = BlogHelper.get_categories_all()

    paginator = PaginatorExt(bloglist, settings.MAIN_LIST_COUNT_PER_PAGE)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render_to_response('Blogs/blog_main_list.html',
                              {"blogs": blogs, "tags": tags, "categories": categories,
                               "comments": BlogHelper.get_blog_comments(),
                               "categories_count": BlogHelper.get_categories_group_count(),
                               'topView': BlogHelper.get_top_view(),
                               "truncateChars": settings.MAIN_LIST_TRUNCATECHARS},
                              context_instance=RequestContext(request))


def blog_show(request, url=''):
    """
    return single blog by blog id
    """
    try:
        id = BlogHelper.get_id_by_url(url)
        blog = BlogHelper.get_blog(id)
        keywords = BlogHelper.get_blog_keywords(id)
        tags = BlogHelper.get_tags_all()
        categories = BlogHelper.get_categories_all()
    except Article.DoesNotExist:
        raise Http404
    return render_to_response("Blogs/blog_show.html",
                              {"blog": blog, "tags": tags, "categories": categories,
                               "domain": settings.DOMAIN_ADDRESS + str(request.get_full_path()),
                               "categories_count": BlogHelper.get_categories_group_count(),
                               'topView': BlogHelper.get_top_view(),
                               "keywords": keywords, "showCatalogue": True},
                              context_instance=RequestContext(request))


def blog_filter_tag(request, tagname=''):
    """
    return blog list filter by tag
    """
    try:
        categories = BlogHelper.get_categories_all()
        tags = BlogHelper.get_tags_all()
        tag = tags.get(tag_name=tagname)
        blogs = BlogHelper.get_bloglist_by_tag(tag)
    except Article.DoesNotExist:
        raise Http404
    return render_to_response("Blogs/blog_filter_tag.html",
                              {"blogs": blogs, "currentTag": tag, "categories": categories, "tags": tags,
                               "comments": BlogHelper.get_blog_comments(),
                               "categories_count": BlogHelper.get_categories_group_count(),
                               'topView': BlogHelper.get_top_view(),
                               "truncateChars": settings.FILTER_TAG_TRUNCATECHARS},
                              context_instance=RequestContext(request))


def blog_filter_category(request, categoryname=''):
    """
    return blog list filter by category
    """
    try:
        categories = BlogHelper.get_categories_all()
        category = categories.get(category_name=categoryname)
        blogs = BlogHelper.get_bloglist_by_category(category)
        tags = BlogHelper.get_tags_all()
    except Article.DoesNotExist:
        raise Http404
    return render_to_response("Blogs/blog_filter_category.html",
                              {"blogs": blogs, "currentCategory": category, "categories": categories, "tags": tags,
                               "comments": BlogHelper.get_blog_comments(),
                               "categories_count": BlogHelper.get_categories_group_count(),
                               'topView': BlogHelper.get_top_view(),
                               "truncateChars": settings.FILTER_CATEGORY_TRUNCATECHARS},
                              context_instance=RequestContext(request))


@requires_csrf_token
def blog_search(request):
    """
    return blog list filter by search keyword
    """
    tags = BlogHelper.get_tags_all()
    categories = BlogHelper.get_categories_all()

    if 'txtSearch' in request.POST:
        txtSearch = request.POST['txtSearch']
        blogs = BlogHelper.get_bloglist_by_search(txtSearch)
        searchResult = Search(blogs.count(), txtSearch)
        return render_to_response('Blogs/blog_search.html',
                                  {"blogs": blogs, "tags": tags, "categories": categories,
                                   "comments": BlogHelper.get_blog_comments(),
                                   "categories_count": BlogHelper.get_categories_group_count(),
                                   'topView': BlogHelper.get_top_view(),
                                   "searchResult": searchResult},
                                  context_instance=RequestContext(request))
    else:
        blogs = BlogHelper.get_bloglist_all()
        return render_to_response("Blogs/blog_search.html",
                                  {"blogs": blogs, "tags": tags,
                                   "comments": BlogHelper.get_blog_comments(),
                                   "categories_count": BlogHelper.get_categories_group_count(),
                                   'topView': BlogHelper.get_top_view()},
                                  context_instance=RequestContext(request))


def page_not_found(request):
    return render_to_response('Function/404.html')


def page_error(request):
    return render_to_response('Function/500.html')


def page_about(request):
    return render_to_response("Blogs/about.html")

