from django.contrib import admin
from models import *
# Register your models here.
import sys

reload(sys);
sys.setdefaultencoding("utf8")

class UserAdmin(admin.ModelAdmin):
	list_diplay = ('username', 'date_joined', 'profile')

class PictureAdmin(admin.ModelAdmin):
	list_diplay = ('Picture_id', 'Image', 'Uploader', 'Upload_date')

admin.site.register(User, UserAdmin)
admin.site.register(Picture, PictureAdmin)
