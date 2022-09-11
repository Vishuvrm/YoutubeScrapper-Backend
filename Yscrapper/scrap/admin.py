from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import VideoComments, YoutubeScrappedData, ChannelData, DownloadedVideos

admin.site.register(ChannelData)
admin.site.register(YoutubeScrappedData)
admin.site.register(VideoComments)
admin.site.register(DownloadedVideos)