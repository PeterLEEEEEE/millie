from django.db import models

from core.models import TimeStamp


class User(TimeStamp):
    nickname          = models.CharField(max_length = 45, unique = True)
    profile_image_url = models.CharField(max_length = 500)
    social_id         = models.CharField(max_length = 100)
    platform          = models.ForeignKey("Platform", on_delete = models.CASCADE)

    class Meta:
        db_table = "users"

class Platform(TimeStamp):
    name      = models.CharField(max_length = 45)

    class Meta:
        db_table = "platforms"