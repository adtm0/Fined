from django import forms
from .models import Wallet, Transaction
from datetime import date

class WalletForm(forms.ModelForm):
  class Meta:
    model = Wallet
    fields = ['name']
    
class TransactionForm(forms.ModelForm):
  class Meta:
    model = Transaction
    fields = ['type', 'amount', 'description', 'date']
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['date'].initial = date.today()
    self.fields['date'].initial = date.today()