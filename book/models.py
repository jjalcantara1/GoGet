from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)

# Create your models here.
