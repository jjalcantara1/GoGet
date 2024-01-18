from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import *

admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
