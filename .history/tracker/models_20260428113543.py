from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Account(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
  
  def __str__(self):
    return self.name

class Transaction(models.Model):
  user = models.ForeignKey(Wallet, on_delete=CASCADE)
  TYPE_CHOICES = [
    ('income', 'Income'),
    ('expense', 'Expense')
  ]
  type = models.CharField(max_length=10, choices=TYPE_CHOICES)
  amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
  description = models.CharField(max_length=100)
  date = models.DateField(default=(timezone.now )