from django.db import models
from datetime import datetime, timedelta, date
import time


# Create your models here.
class ChannelData(models.Model):
    channel_link = models.TextField(primary_key=True)
    num_videos = models.BigIntegerField(default=0, blank=False)
    time_of_scrapping = models.DateTimeField(blank=False, default=datetime.now())

    def __str__(self):
        return self.channel_link
    
    @classmethod
    def filter(cls, *args, **kwargs):
        res = cls.objects.filter(*args, **kwargs).first()
        response = {}
        if res:
            response["channel_link"] = res.channel_link
            response["num_videos"] = res.num_videos
        return response
    
    @classmethod
    def get_all_records(cls):
        return cls.objects.all()
    
    @classmethod
    def update_time(cls, *args, **kwargs):
        res = cls.objects.filter(*args, **kwargs)
        res.update(time_of_scrapping = datetime.now())
    
    @classmethod
    def delete_record(cls, *args, **kwargs):
        instance = cls.objects.get(*args, **kwargs)
        instance.delete()
    
    @classmethod
    def get_length(cls):
        return cls.objects.all().count()
    
    @classmethod
    def delete_scheduled_records(cls):
        channel_records = cls.get_all_records()
         
        for channel in channel_records:
            channel_link = channel.channel_link
            creation_time = channel.time_of_scrapping.strftime("%H:%M:%S")
            current_time = datetime.now().strftime("%H:%M:%S")

            time_interval = datetime.strptime(current_time, "%H:%M:%S") - datetime.strptime(creation_time, "%H:%M:%S")
            total_seconds_from_creation = abs(time_interval.total_seconds())


            if total_seconds_from_creation > 5*60*60:
                cls.delete_record(channel_link = channel_link)
        


class YoutubeScrappedData(models.Model):
    channel_link = models.ForeignKey(ChannelData, default=1, verbose_name="channel_link", on_delete=models.CASCADE) 
    video_link = models.TextField(primary_key=True)
    author = models.CharField(max_length=500, blank=False, default='')   
    title = models.CharField(max_length=500, blank=False, default='') 
    likes = models.CharField(max_length=20, blank=False, default='')
    thumbnail = models.TextField(blank=False, default='')
    # download_link = models.TextField(blank=False, default="")

    def __str__(self):
        return self.title
    
    @classmethod
    def filter(cls, qty,  *args, **kwargs):
        res = cls.objects.filter(*args, **kwargs).all()
        response = {}
        i = 0
        for r in res:
            if i < qty:
                response[r.video_link] = { 
                "channel_link": r.channel_link.pk,
                "title": r.title,
                "author":r.author,
                "likes": r.likes,
                "thumbnail": r.thumbnail
                }
            i += 1
            
        return response
    
    @classmethod
    def get_length(cls):
        return cls.objects.all().count()
    
    


class VideoComments(models.Model):
    video_link = models.ForeignKey(YoutubeScrappedData, default=1, verbose_name="video_link", on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=200, blank=True, default="Author")
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.commenter_name

    @classmethod
    def get_comments(cls, url, *args, **kwargs):
        res = cls.objects.filter(video_link=url).all()
        response = []
        for r in res:
            data = {}
            if r.commenter_name:
                data["commenter_name"] = r.commenter_name
            else:
                data["commenter_name"] = "Author"
            
            data["comment"] = r.comment
            
            response.append(data)
        return response


class DownloadedVideos(models.Model):
    video_link = models.TextField(blank=False)
    download_link = models.TextField(blank=False)

    def __str__(self):
        return self.download_link
    
    @classmethod
    def get_download_link(cls, url):
        res = cls.objects.filter(video_link=url).first()
        response = {}

        if res:
            response["video_link"] = res.video_link
            response["download_link"] = res.download_link
        
        return response

