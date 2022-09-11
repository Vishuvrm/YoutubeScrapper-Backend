from rest_framework import serializers
from .models import YoutubeScrappedData, VideoComments, ChannelData, DownloadedVideos
from marshmallow import Schema, fields

class ChannelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelData
        fields = ("channel_link", "num_videos")


class YoutubeScrappedDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = YoutubeScrappedData
        fields = ("video_link", "channel_link", "title", "author", "likes", "thumbnail")


class VideoCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoComments
        fields = ("video_link", "commenter_name", "comment")

class DownloadedVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadedVideos
        fields = ("video_link", "download_link")


class ValidationException(Exception):

    def __init__(self, msg="", msg_code="", status="", errors=None):
        self.msg = msg
        self.msg_code = msg_code
        self.errors = errors
        self.status = status
        super().__init__(msg)

    def get_errors(self):
        return self.errors
