from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  balance = models.DecimalField(max_)