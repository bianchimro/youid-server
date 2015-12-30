from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from jsonfield import JSONField


class ApplicationUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)


class Device(models.Model):
    device_id = models.CharField(max_length=200)
    application_user = models.ForeignKey(ApplicationUser)


class ApplicationUserData(models.Model):
    application_user = models.ForeignKey(ApplicationUser)    
    key = models.CharField(max_length=200)
    value = JSONField(null=True, blank=True)

    


