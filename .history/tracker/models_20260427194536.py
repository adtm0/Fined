from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
  
  def __str__(self):
    return self.name

class Transaction(models.Model):
  user = models.ForeignKey(Wallet, on_delete=CASCADE)
  type = models.CharField(max_length=10, choices=TYPE_CHOICES)
  TYPE_CHOICES = [
    ('inc')
  ]
  amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
  description = models.CharField(max_length=100)
  date = models.DateField(default=)