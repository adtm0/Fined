from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from .forms import WalletForm, TransactionForm

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
  total_balance = sum(wallet.balance for wallet in wallets)
  recent_transactions = Transaction.objects.filter(
    wallet__user=request.user
  ).order_by('-date')[:5]
  return render(request, 'tracker/dashboard.html', {
    'wallets': wallets,
    'total_balance': total_balance
    })

@login_required
def add_wallet(request):
  if request.method == 'POST':
    form = WalletForm(request.POST)
    if form.is_valid():
      wallet = form.save(commit=False)
      wallet.user = request.user
      wallet.save()
      return redirect('dashboard')
  else:
    form = WalletForm()
  return render(request, 'tracker/add_wallet.html', {'form': form})
      
@login_required
def add_transaction(request, wallet_id):
  wallet = Wallet.objects.get(id=wallet_id, user=request.user)
  if request.method == 'POST':
    form = TransactionForm(request.POST)
    if form.is_valid():
      transaction = form.save(commit=False)
      transaction.wallet = wallet
      transaction.save()
      
      if transaction.type == 'income':
        wallet.balance += transaction.amount
      else:
        wallet.balance -= transaction.amount
      
      wallet.save()
      return redirect('dashboard')
  
  else:
    form = TransactionForm()
    
  return render(request, 'tracker/add_transaction.html', {'form': form, 'wallet': wallet})

@login_required
def wallet_detail(request, wallet_id):
  wallet = Wallet.objects.get(id=wallet_id,user=request.user)
  transactions = Transaction.objects.filter(wallet=wallet)
  return render(request, 'tracker/wallet_detail.html', {'wallet': wallet, 'transactions': transactions})

@login_required
def edit_transaction(request, transaction_id):
  transaction = Transaction.objects.get(id=transaction_id, wallet__user=request.user)
  old_amount = transaction.amount
  old_type = transaction.type
  if request.method == 'POST':
    form = TransactionForm(request.POST, instance=transaction)
    if form.is_valid():
      wallet = transaction.wallet
      if old_type == 'income':
        wallet.balance -= old_amount
      else:
        wallet.balance += old_amount
      transaction = form.save()
      if transaction.type == 'income':
        wallet.balance += transaction.amount
      else:
        wallet.balance -= transaction.amount
      wallet.save()
      return redirect('wallet_detail', wallet_id=wallet.id)
  else:
    form = TransactionForm(instance=transaction)
  return render(request, 'tracker/edit_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def delete_transaction(request, transaction_id):
  transaction  = Transaction.objects.get(id=transaction_id, wallet__user=request.user)
  wallet = transaction.wallet
  if transaction.type == 'income':
    wallet.balance -= transaction.amount
  else:
    wallet.balance += transaction.amount
  wallet.save()
  transaction.delete()
  return redirect('wallet_detail', wallet_id=wallet.id)

@login_required
def edit_wallet(request, wallet_id):
  wallet = Wallet.objects.get(id=wallet_id, user=request.user)
  if request.method =='POST':
    form = WalletForm(request.POST, instance=wallet)
    if form.is_valid():
      form.save()
      return redirect('dashboard')
  else:
    form = WalletForm(instance=wallet)
  return render(request, 'tracker/edit_wallet.html', {'form': form, 'wallet': wallet})

@login_required
def delete_wallet(request, wallet_id):
  wallet = Wallet.objects.get(id=wallet_id, user=request.user)
  wallet.delete()
  return redirect('dashboard')