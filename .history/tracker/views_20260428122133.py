from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request)