from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from Services.models import Comment, Evaluation, Announcement
from Services.serializers import CommentSerializer, EvaluationSerializer, AnnouncementSerializer
from Utility.UtilityHelper import HTTPHelper, CommentHelper
from blog.blogHelper import BlogHelper

import datetime

KEY_BLOGLIST = 'blog_list'
KEY_TAGS = 'tags'
KEY_CATEGORIES = 'categories'
KEY_BLOG_PREFIX = 'blog_'
KEY_TOP_VIEW = 'top_view'


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET'])
def comment_list(request):
    """
    List all comments in terms of an article
    """
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return JSONResponse(serializer.data)


@api_view(['GET'])
def clear_caches(request):
    if request.method == 'GET':
        try:
            if str(request.GET.get('token', '')) == 'WillHu':
                BlogHelper.clear_caches(KEY_BLOGLIST, KEY_TAGS, KEY_CATEGORIES, KEY_TOP_VIEW)
        except:
            pass
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def clear_cache(request):
    if request.method == 'GET':
        try:
            if str(request.GET.get('token', '')) == 'WillHu' \
                    and request.GET.get('id', '') is not None:
                BlogHelper.clear_caches(KEY_BLOG_PREFIX + str(request.GET.get('id', '')))
        except:
            pass
    return Response(status=status.HTTP_204_NO_CONTENT)


@requires_csrf_token
@api_view(['GET', 'POST', 'DELETE'])
def comment_detail(request, pk):
    """
    Retrieve, update or delete a comment instance.
    """
    try:
        # ToDo: this method would sync to Cache some time later
        comment = Comment.objects.filter(article_id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(comment, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        if CommentHelper.refresh_ip_comment(request, pk) and CommentHelper.validate_ip_comment(request, pk):
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                ip = HTTPHelper.get_client_ip(request)
                serializer.save(userIp=ip)

                messageContent = dict(request.data).get("messageContent")[0]
                userName = dict(request.data).get("userName")[0]
                userContact = dict(request.data).get("userContact")[0]

                BlogHelper.send_comment_mail(pk, userName, messageContent, ip, userContact)
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response('201')
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # serializer.is_valid()
            return Response('400')
        return Response('406')  # validate_ip_comment

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@requires_csrf_token
@api_view(['GET', 'POST'])
def evaluation_detail(request, pk):
    """
    Retrieve, update or delete a evaluation instance.
    """
    try:
        # ToDo: this method would sync to Cache some time later
        evaluation = Evaluation.objects.filter(article_id=pk).first()
    except Evaluation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get viewCount & praiseCount
    if request.method == 'GET':
        serializer = EvaluationSerializer(evaluation, many=False)
        return JSONResponse(serializer.data)

    # would distinguish different post from ViewCount & PraiseCount
    elif request.method == 'POST':
        serializer = EvaluationSerializer(evaluation, data=request.data)
        if serializer.is_valid():
            try:
                requestType = request.data['type']
            except KeyError:
                pass

            # Init default value when first time
            if evaluation is None:
                evalView = 0
                evalPraise = 0
            else:
                evalView = evaluation.viewCount
                evalPraise = evaluation.praiseCount

            if requestType == "view":
                serializer.save(viewCount=evalView+1)
            elif requestType == "praise":
                if CommentHelper.validate_ip_praise(request, pk):
                    serializer.save(praiseCount=evalPraise+1)
                    BlogHelper.send_praise_mail(pk)
                else:
                    return Response('406')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('400')


@api_view(['GET'])
def announcement_detail(request):

    try:
        announcement = BlogHelper.get_announcement()
        if announcement is None:
            announcement = Announcement.objects.filter(startDate__lte=datetime.datetime.now(),
                                                    endDate__gte=datetime.datetime.now()).first()
            BlogHelper.set_announcement(announcement)

    except Announcement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AnnouncementSerializer(announcement, many=False)
        return JSONResponse(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)