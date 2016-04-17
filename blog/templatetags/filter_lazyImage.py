__author__ = 'will'
# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
import re

register = template.Library()


@register.filter(name='filter_lazyImage')
def filter_lazyImage(value):
    """
    filter_lazyImage is to replace the content from "src" to "data-original"
    """
    try:
        arg = "class=\"lazy\" src="
        if re.search(arg.encode("utf8"), value.encode("utf8"), re.M | re.I | re.U):
            return re.sub(arg, "class=\"lazy\" data-original=", value)
        else:
            return value
    except ValueError:
        pass
        return value