# models.py

from django.db import models
from django.utils import timezone

from adminpanel.models import RoomType


# class TemporaryHold(models.Model):
#     room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
#     held_until = models.DateTimeField()
#
#     def is_valid(self):
#         return timezone.now() < self.held_until

