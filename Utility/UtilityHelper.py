# -*- coding: utf-8 -*-
from ipware.ip import get_real_ip
from django.core.cache import cache
from datetime import datetime, timedelta


IPPool_Praise = []
IPPool_Comment = {}     # Dictionary
TimeSpan_Comment_Frequency_Interval = 15


class HTTPHelper:
    """
    HTTP helper wrapper
    """

    def __init__(self):
        pass

    @staticmethod
    def get_client_ip(request):
        """
        Get the client ip from the request
        """
        ip = get_real_ip(request)
        # ip = str(randrange(1, 2))
        if ip is None:
            ip = '0.0.0.0'
        return ip


class CommentHelper:
    """
    Comment helper wrapper
    """

    def __init__(self):
        pass

    @staticmethod
    def validate_ip_praise(request, pk):
        """
        Each IP is only allowed to praise once in terms of each article
        """
        ip = HTTPHelper.get_client_ip(request)
        key = ip + '_' + str(pk)
        global IPPool_Praise
        if key not in IPPool_Praise:
            IPPool_Praise.append(key)
            return True
        return False

    @staticmethod
    def validate_ip_comment(request, pk):
        """
        Each IP is only allowed to comment once for each article in CERTAIN period
        """
        ip = HTTPHelper.get_client_ip(request)
        key = ip + '_' + str(pk)    # key is the IP_articleId
        global IPPool_Comment
        if key not in IPPool_Comment.keys():
            IPPool_Comment[key] = datetime.utcnow()
            return True
        return False

    @staticmethod
    def refresh_ip_comment(request, pk):
        """
        The function indicates one IP may comment on one article more than
        every 15 seconds. Each proper record in the Dictionary would be remove through this function.
        The function is used every time right before validate_ip_comment
        """
        ip = HTTPHelper.get_client_ip(request)
        key = ip + '_' + str(pk)    # key is the IP_articleId
        global IPPool_Comment
        if key in IPPool_Comment.keys():
            perviousTimeStamp = IPPool_Comment[key]
            currentTimeStamp = datetime.utcnow()
            if currentTimeStamp >= perviousTimeStamp + timedelta(seconds=TimeSpan_Comment_Frequency_Interval):
                del IPPool_Comment[key]
        return True


class RedisHelper:
    """
    Redis helper wrapper
    """

    def __init__(self):
        pass

    @staticmethod
    def create_cache(key, value, timeout):
        cache.set(key, value, timeout)

    @staticmethod
    def get_cache(key):
        return None if cache.get(key) is None else cache.get(key)

    @staticmethod
    def is_cache_exist(key):
        return False if cache.get(key) is None else True

    @staticmethod
    def delete_cache(key):
        if cache.get(key) is not None:
            cache.delete(key)

    @staticmethod
    def clear_all_cache(*args):
        for key in args:
            if cache.get(key) is not None:
                cache.delete(key)


class RedisTimeOut:
    """
    Redis Time out enum settings
    """

    def __init__(self):
        pass

    REDIS_TIMEOUT_10_SEC = 10
    REDIS_TIMEOUT_30_SEC = 10
    REDIS_TIMEOUT_ONE_MIN = 60
    REDIS_TIMEOUT_5_MIN = 5 * 60
    REDIS_TIMEOUT_ONE_HOUR = 60 * 60
    REDIS_TIMEOUT_HALF_DAY = 12 * 60 * 60
    REDIS_TIMEOUT_1_DAYS = 24 * 60 * 60
    REDIS_TIMEOUT_7_DAYS = 7 * 24 * 60 * 60
    REDIS_TIMEOUT_1_MONTH = 30 * 24 * 60 * 60
    NEVER_REDIS_TIMEOUT = 365 * 24 * 60 * 60