from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
