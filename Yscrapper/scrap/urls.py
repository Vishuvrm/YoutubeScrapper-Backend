from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from scrap.views import GetYoutubeVideos, GetComments, DownloadVideo

urlpatterns = [
    path('get-videos', GetYoutubeVideos.as_view(), name='videos'),
    path('get-comments', GetComments.as_view(), name="comments"),
    path('download-video', DownloadVideo.as_view(), name="download")
]