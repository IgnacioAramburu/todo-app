from django.shortcuts import render,redirect
from django.contrib.auth import logout

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')
