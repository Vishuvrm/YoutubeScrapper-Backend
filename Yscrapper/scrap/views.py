from cgitb import reset
from curses.ascii import HT
import http
import os
import re
# from turtle import title
from rest_framework import generics
from django.forms.models import model_to_dict
from .models import VideoComments, YoutubeScrappedData, ChannelData, DownloadedVideos
from .serializers import VideoCommentsSerializer, YoutubeScrappedDataSerializer, ChannelDataSerializer, DownloadedVideosSerializer
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status
from .service import *
from .creds.quickstart import authorize_gdrive_creds
from .upload_to_drive import upload_single_file
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Create your views here.


class GetYoutubeVideos(generics.ListCreateAPIView):
   serializer_class = ChannelDataSerializer
   def get(self, request, format=None):
        return HttpResponse("<h1>Request working!!</h1>")

   def post(self, request, format=None):
      "video_link", "author", "title", "likes", "thumbnail"
      request_data = request.data
      channel_link = request_data["channel_link"]
      num_videos = int(request_data["num_videos"])
      request_data["num_videos"] = num_videos

      request_serializer = self.serializer_class(data=request_data)
      # Check if link already exists in the database
      channel_stored_data = ChannelData.filter(channel_link = channel_link)
      if channel_stored_data:
         ChannelData.update_time(channel_link = channel_link)
         channel_stored_data_num_videos = channel_stored_data["num_videos"]
         if num_videos <= channel_stored_data_num_videos and YoutubeScrappedData.get_length() == channel_stored_data_num_videos:
            response = YoutubeScrappedData.filter(channel_link=request_data["channel_link"], qty = request_data["num_videos"])
            return Response(response, status=status.HTTP_200_OK)

         # Clean the records
         ChannelData.delete_record(channel_link = channel_link)


      if request_serializer.is_valid(raise_exception=True):
            request_serializer.save()
      else:
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      response = get_channel_videos_data(channel_link=channel_link, num_videos=num_videos)


      for video_link in response:
         try:
            final_response = {}
            final_response["video_link"] = video_link
            final_response.update(response[video_link])
            video_serializer = YoutubeScrappedDataSerializer(data=final_response)
            if video_serializer.is_valid(raise_exception=True):
               video_serializer.save()
         except:
            break
      else:
         return Response(response, status=status.HTTP_201_CREATED)
      
      return Response(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetComments(generics.ListCreateAPIView):
   serializer_class = VideoCommentsSerializer

   def post(self, request, format=None):
      "video_link", "commenter_name", "comment"
      url = request.data["url"]

      # Initial check
      sample_response = {"video_link": url, "commenter_name": "_", "comment": "_"}
      comment_serializer = self.serializer_class(data = sample_response)
      if comment_serializer.is_valid(raise_exception=True):
         comments = VideoComments.get_comments(url)
         if comments:
            return Response(comments, status=status.HTTP_200_OK)
         comments = get_comments(url)
      else:
         return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      for comment in comments:
         try:
            comment["video_link"] = url
            comment["commenter_name"] = "Author" if not comment["commenter_name"] else comment["commenter_name"]
               
            comment_serializer = self.serializer_class(data = comment)

            if comment_serializer.is_valid(raise_exception=True):
               comment_serializer.save()
            
         except Exception as e:
            print(e)
            break
      else:
         # final_comments_response = {"video_link": url, "comments_data": comments}
         return Response(VideoComments.get_comments(url), status=status.HTTP_201_CREATED)
      return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DownloadVideo(generics.ListCreateAPIView):
   serializer_class = DownloadedVideosSerializer

   def post(self, request, format=None):
      url = request.data["url"]
      saved_download_link_response = DownloadedVideos.get_download_link(url)
      if saved_download_link_response:
         return Response(saved_download_link_response, status=status.HTTP_200_OK)
         
      video_title = YoutubeScrappedData.objects.filter(video_link = url).first().title + ".mp4"
      video_title = re.sub(r'[/\:*?"<>|]', "~", video_title)
      service =authorize_gdrive_creds()
      # location = r'D:\personal\YoutubeScrapperProject\Yscrapper\static\Videos'
      location = os.path.abspath(r"Yscrapper\scrap\static\videos")
      src = os.path.join(location, video_title)
      success = download_video(url=url, location=location, filename=video_title)
      
      if success:
         gdrive_url = upload_single_file(service, src, video_title)
         os.remove(src)
         response = {"video_link": url, "download_link": gdrive_url}
         download_record = self.serializer_class(data=response)
         if download_record.is_valid():
            download_record.save()
            return Response(response, status=status.HTTP_200_OK)

      return Response({"msg": "Video download failed!"}, status.HTTP_400_BAD_REQUEST)

      