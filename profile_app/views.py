from django.shortcuts import render,redirect
from .models import profile
from django.contrib import auth
from django.contrib.auth.models import User

def home(request):
    template = 'base.html'
    context = {}
    if request.user.is_authenticated:
        obj = profile.objects.get(user=request.user)
        context['profile'] = obj
    return render(request,template,context)

def login(request):
    template = 'profile/login.html'
    context = {}
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']
        try:
            userobj = User.objects.get(username=a)
        except:
            context['message'] = 'User does not exist!'
            return render(request,template,context)
        if userobj.check_password(b):
            auth.login(request,userobj)
            return redirect('/')
        else:
            context['message'] = 'Password not correct!'
            return render(request,template,context)
    return render(request,template,context)

def logout(request):
    auth.logout(request)
    return redirect('/')