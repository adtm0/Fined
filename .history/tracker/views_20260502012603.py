from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import calendar
from .models import Account, Transaction, Activity
from .forms import AccountForm, TransactionForm

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
  accounts = Account.objects.filter(user=request.user)
  total_balance = sum(account.balance for account in accounts)
  
  all_transactions = Transaction.objects.filter(account__user=request.user)
  total_income = sum(t.amount for t in all_transactions if t.type == 'income')
  total_spending = sum(t.amount for t in all_transactions if t.type == 'expense')
  
  if total_income > 0:
    savings_rate = round((total_income - total_spending) / total_income * 100)
  else:
    savings_rate = 0
  
  recent_transactions = Transaction.objects.filter(
    account__user=request.user
  ).order_by('-date')[:5]
  
  last_7_days = [date.today() - timedelta(days=i) for i in range(6, -1, -1)]
  chart_labels = [d.strftime('%b %d') for d in last_7_days]
  chart_income = []
  chart_expense = []
  for day in last_7_days:
    transactions = Transaction.objects.filter(account__user=request.user, date=day)
    income = sum(t.amount for t in transactions if t.type == 'income')
    expense = sum(t.amount for t in transactions if t.type == 'expense')
    chart_income.append(float(income))
    chart_expense.append(float(expense))
    
  cal_year = int(request.GET.get('year', date.today().year))
  cal_month = int(request.GET.get('month', date.today().month))
  
  cal = calendar.Calendar(firstweekday=6)
  calendar_weeks = cal.monthdayscalendar(cal_year, cal_month)
  calendar_month_name = date(cal_year, cal_month, 1).strftime('%B %Y')
  today_day = date.today().day if (cal_year == date.today().year and cal_month == date.today().month) else 0
  
  
  prev_month = cal_month - 1 if cal_month > 1 else 12
  prev_year = cal_year if cal_month > 1 else cal_year - 1
  next_month = cal_month + 1 if cal_month < 12 else 1
  next_year = cal_year if cal_month < 12 else cal_year + 1
  
  month_transactions = Transaction.objects.filter(
    account__user=request.user,
    date__year=cal_year,
    date__month=cal_month
  )
  income_days = set()
  expense_days = set()
  for t in month_transactions:
    if t.type == 'income':
      income_days.add(t.date.day)
    else:
      expense_days.add(t.date.day)
  
  return render(request, 'tracker/dashboard.html', {
    'accounts': accounts,
    'total_balance': total_balance,
    'total_income': total_income,
    'total_spending': total_spending,
    'savings_rate': savings_rate,
    'recent_transactions': recent_transactions,
    'chart_labels': chart_labels,
    'chart_income': chart_income,
    'chart_expense': chart_expense,
    'calendar_weeks': calendar_weeks,
    'calendar_month_name': calendar_month_name,
    'today_day': today_day,
    'income_days': income_days,
    'expense_days': expense_days,
    'prev_month': prev_month,
    'prev_year': prev_year,
    'next_month': next_month,
    'next_year': next_year
    })

@login_required
def add_account(request):
  if request.method == 'POST':
    form = AccountForm(request.POST)
    if form.is_valid():
      account = form.save(commit=False)
      account.user = request.user
      account.save()
      
      # Log Activity
      Activity.objects.create(
        user=request.user,
        activity_type='account_created',
        description=f'{account.name} account created'
      )
      return redirect('dashboard')
  else:
    form = AccountForm()
  return render(request, 'tracker/add_account.html', {'form': form})
      
@login_required
def add_transaction(request, account_id):
  account = Account.objects.get(id=account_id, user=request.user)
  if request.method == 'POST':
    form = TransactionForm(request.POST)
    if form.is_valid():
      transaction = form.save(commit=False)
      transaction.account = account
      transaction.save()
      
      if transaction.type == 'income':
        account.balance += transaction.amount
      else:
        account.balance -= transaction.amount
      
      account.save()
      return redirect('dashboard')
  
  else:
    form = TransactionForm()
    
  return render(request, 'tracker/add_transaction.html', {'form': form, 'account': account})

@login_required
def add_transaction_modal(request):
  if request.method == 'POST':
    account_id = request.POST.get('account')
    account = Account.objects.get(id=account_id, user=request.user)
    form = TransactionForm(request.POST)
    print("POST data:", request.POST)
    print("FORM valid:", form.is_valid())
    print("FORM errors:", form.errors)
    if form.is_valid():
      transaction = form.save(commit=False)
      transaction.account = account
      transaction.save()
      if transaction.type == 'income':
        account.balance += transaction.amount
      else: 
        account.balance -= transaction.amount
      account.save()
      
      Activity.objects.create(
        user=request.user
        activity_type='transaction_added'
      )
      
  return redirect('dashboard')

@login_required
def account_detail(request, account_id):
  account = Account.objects.get(id=account_id,user=request.user)
  transactions = Transaction.objects.filter(account=account)
  return render(request, 'tracker/account_detail.html', {'account': account, 'transactions': transactions})

@login_required
def edit_transaction(request, transaction_id):
  transaction = Transaction.objects.get(id=transaction_id, account__user=request.user)
  old_amount = transaction.amount
  old_type = transaction.type
  if request.method == 'POST':
    form = TransactionForm(request.POST, instance=transaction)
    if form.is_valid():
      account = transaction.account
      if old_type == 'income':
        account.balance -= old_amount
      else:
        account.balance += old_amount
      transaction = form.save()
      if transaction.type == 'income':
        account.balance += transaction.amount
      else:
        account.balance -= transaction.amount
      account.save()
      return redirect('account_detail', account_id=account.id)
  else:
    form = TransactionForm(instance=transaction)
  return render(request, 'tracker/edit_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def delete_transaction(request, transaction_id):
  transaction  = Transaction.objects.get(id=transaction_id, account__user=request.user)
  account = transaction.account
  if transaction.type == 'income':
    account.balance -= transaction.amount
  else:
    account.balance += transaction.amount
  account.save()
  transaction.delete()
  return redirect('account_detail', account_id=account.id)

@login_required
def edit_account(request, account_id):
  account = Account.objects.get(id=account_id, user=request.user)
  if request.method =='POST':
    form = AccountForm(request.POST, instance=account)
    if form.is_valid():
      form.save()
      return redirect('dashboard')
  else:
    form = AccountForm(instance=account)
  return render(request, 'tracker/edit_account.html', {'form': form, 'account': account})

@login_required
def delete_account(request, account_id):
  account = Account.objects.get(id=account_id, user=request.user)
  account.delete()
  return redirect('dashboard')

@login_required
def history(request):
  transactions = Transaction.objects.filter(
    account__user=request.user
  ).order_by('-date')
  return render(request, 'tracker/history.html', {'transactions': transactions})