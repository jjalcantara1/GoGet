from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.name}"



