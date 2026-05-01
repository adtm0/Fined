from django import forms
from .models import Wallet, Transaction

class WalletForm(forms.ModelForm):
  class Meta:
    model = Wallet
    fields = ['name']
    
class TransactionForm(forms.ModelForm):
  class Meta:
    model = Transaction
    fields = ['type', 'amount', 'description']