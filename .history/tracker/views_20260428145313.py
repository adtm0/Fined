from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Wallet
from .forms import WalletForm

def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')
  
  else:
    form = UserCreationForm()
  
  return render(request, 'tracker/register.html', {'form': form})

@login_required
def dashboard(request):
  wallets = Wallet.objects.filter(user=request.user)
  return render(request, 'tracker/dashboard.html', {'wallets': wallets})

@login_required
def add_wallet(request):
  if request.method == 'POST':
    if form.is_valid():
      wallet = form.save(commit=False)
      wallet.user = request.user
      wallet.save()
      return redirect('dashboard')
  else:
    
      