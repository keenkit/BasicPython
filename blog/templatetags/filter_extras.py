# -*- coding: utf-8 -*-
from django.conf import settings
from django import template

import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

register = template.Library()


@register.filter(name='filter_extras')
def filter_extras(value, arg):
    """
    filter_extras is to get the content around key word
    """
    try:
        searchTruncateChars = settings.SEARCH_TRUNCATECHARS
        if re.search(arg.encode("utf8"), value.encode("utf8"), re.M | re.I | re.U):
            lowerValue = re.sub(arg, arg.lower(), value, count=1, flags=re.I)
            lowerValueFilterHtmlTags = re.sub(re.compile(r'</?\w+[^>]*>', re.S), '', lowerValue)
            nPos = lowerValueFilterHtmlTags.index(arg.lower())
            startPos = nPos - searchTruncateChars if nPos >= searchTruncateChars else 0
            endPos = nPos + searchTruncateChars
            return re.sub(arg, "<span class='searchResult'>"+arg+"</span>",
                          lowerValueFilterHtmlTags[startPos:endPos],
                          flags=re.I)
        else:
            return value
    except ValueError:
        pass
        return ''