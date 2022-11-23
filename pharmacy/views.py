from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from .decorators import *


@unautheticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('/')

        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')
