from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegisterForm, LoginUserForm
from e_store.models import Address
from accounts.models import User
from django.views.generic.base import RedirectView
from django.contrib import messages
# Create your views here.

def register_account(request):
    context = {}
    if request.POST: 
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            message.success(request, 'Registered successfully')
            return redirect('store:store_view')
        else:
            context['form_set'] = form
    else:
        form = RegisterForm()
        context['form_set'] = form
    return render(request, 'accounts/register.html', context)

def logout_account(request):
    logout(request)
    return render(request, 'accounts/logout.html')




def login_account(request):
    user = request.user
    if user.is_authenticated:
        return redirect('store:store_view')
    context = {}
    if request.POST:
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "Login successful")
                return redirect('store:store_view')
        else:
            form = LoginUserForm(request.POST)
            context['form'] = form
    else: #GET request
        form = LoginUserForm()
        context['form'] = form
    return render(request, 'accounts/login.html', context)
    
    


