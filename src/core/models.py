from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)


class Site(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()


class TrafficStatistics(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    page_views = models.IntegerField(default=0)
    data_sent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    data_received = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
