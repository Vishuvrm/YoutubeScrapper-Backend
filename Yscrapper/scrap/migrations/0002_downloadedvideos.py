# Generated by Django 4.1 on 2022-09-10 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scrap", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DownloadedVideos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("video_link", models.TextField()),
                ("download_link", models.TextField()),
            ],
        ),
    ]
