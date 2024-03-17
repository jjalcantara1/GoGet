from django.db import models
from django.utils import timezone

class Promo(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    max_redemptions = models.PositiveIntegerField(default=1)
    times_redeemed = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.code