from django.db import models
from django.contrib.auth.models import User
import random, string

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Awaiting pickup'),
        ('confirmed', 'Confirmed / Paid'),
        ('cancelled', 'Cancelled'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    item_id    = models.CharField(max_length=50)
    item_name  = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    code       = models.CharField(max_length=8, default=generate_code, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} — {self.item_name}"