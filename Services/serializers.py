from rest_framework import serializers
from Services.models import Comment, Evaluation, Announcement
from stripogram import html2text, html2safehtml

class CommentSerializer(serializers.ModelSerializer):
    # messageContent = serializers.CharField()
    # created = serializers.DateTimeField(required=False)
    # userName = serializers.CharField()
    # userContact = serializers.CharField(required=False, allow_blank=True)
    # userIp = serializers.CharField(required=False, allow_blank=True)
    # isValid = serializers.BooleanField(default=True)
    # article_id = serializers.IntegerField()

    class Meta:
            model = Comment
            fields = ('messageContent', 'created', 'userName', 'userContact', 'userIp', 'isValid', 'article_id')

    def create(self, validated_data):
        comment = validated_data[u'messageContent']
        userName = validated_data[u'userName']
        userContact = validated_data[u'userContact']
        validated_data[u'messageContent'] = html2safehtml(comment, valid_tags=("b", "a", "i", "br", "p", "pre"))
        validated_data[u'userName'] = html2safehtml(userName, valid_tags=("b", "a", "i", "br", "p", "pre"))
        validated_data[u'userContact'] = html2safehtml(userContact, valid_tags=("b", "a", "i", "br", "p", "pre"))
        return Comment.objects.create(**validated_data)


class EvaluationSerializer(serializers.ModelSerializer):
    # viewCount = serializers.IntegerField(required=False)
    # praiseCount = serializers.IntegerField(required=False)
    # article_id = serializers.IntegerField()

    class Meta:
            model = Evaluation
            fields = ('viewCount', 'praiseCount', 'article_id')

    def create(self, validated_data):
        return Evaluation.objects.update_or_create(**validated_data)


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
            model = Announcement
            fields = ('announcement', 'startDate', 'endDate')