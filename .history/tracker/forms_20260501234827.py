from django import forms
from .models import Account, Transaction
from datetime import date

class AccountForm(forms.ModelForm):
  class Meta:
    model = Account
    fields = ['name']
    
class TransactionForm(forms.ModelForm):
  class Meta:
    model = Transaction
    fields = ['type', 'amount', 'description', 'date']
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['date'].initial = date.today()
    self.fields['description'].required = False