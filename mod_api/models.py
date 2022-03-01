from django.contrib.auth.models import User
from django.db import models

from datetime import timedelta, datetime


class News(models.Model):
    location = models.URLField()
    headline = models.TextField()
    # source could be given choices as well but get that from config file for now
    source = models.CharField(max_length=10, choices=(('reddit', 'reddit'), ('newsapi', 'newsapi')))
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField()
    users = models.ManyToManyField(User, through='UserFavouriteNews')

    @staticmethod
    def expiration_time_calculation():
        expiration_duration = 86400  # time in seconds,must come from Source object
        expiration_time = datetime.now() + timedelta(seconds=expiration_duration)
        return expiration_time

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = self.expiration_time_calculation()
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline

class UserFavouriteNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    favourite = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
