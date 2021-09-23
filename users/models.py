from core.models import TimeStamp
from django.db import models


class User(TimeStamp):
    nickname          = models.CharField(max_length = 45, unique = True)
    phone_number      = models.CharField(max_length = 20)
    profile_image_url = models.CharField(max_length = 500)
    flatform          = models.ForeignKey("Flatform", on_delete = models.CASCADE)
    
    class Meta:
        db_table = "users"

class Flatform(TimeStamp):
    name      = models.CharField(max_length = 45)
    social_id = models.IntegerField()

    class Meta:
        db_table = "flatforms" 