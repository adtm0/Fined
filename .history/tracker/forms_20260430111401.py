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
    
  def __init__(self, data = ..., files = ..., auto_id = ..., prefix = ..., initial = ..., error_class = ..., label_suffix = ..., empty_permitted = ..., instance = ..., use_required_attribute = ..., renderer = ...):
    super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance, use_required_attribute, renderer)