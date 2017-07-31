from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import os
# Create your models here.

class User(AbstractUser):    
    profile = models.CharField('profile', default='', max_length=256, blank = True)
 
    def __str__(self):
        return self.username

def upload_to_path(instance, filename):
	return '/'.join(['img', str(instance.project), filename])

class Picture(models.Model):
	project = models.CharField(default='', max_length=30)
	name = models.CharField('Name', default = '', max_length=30)
	Image = models.ImageField(upload_to = upload_to_path)
	uploader = models.ForeignKey(User, null = True, on_delete = models.CASCADE, 
		 blank = True, default = None)
	up_load_date = models.DateTimeField(auto_now = True, null=True)

	def __str__(self):
		return self.name
