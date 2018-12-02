from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect

from .models import ActivationProfile
from .models import NorthUser

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import UserLoginForm, RegisterForm

#code to activate inactive user
def activate_user(request,code=None):
    if code:
        qs = ActivationProfile.objects.filter(key=code)
        if qs.exists() and qs.count() == 1:
             obj = qs.first()
             if not obj.expired:
                 usr = obj.user
                 usr.is_active = True
                 usr.save()
                 obj.expired = True
                 obj.save()
                 return redirect('/accounts/login')
    else:
        raise Http404

#Code to login a user
def login_view(request):
    form = UserLoginForm(request.POST or None)
    template_name = 'accounts/login.html'
    context = {'form': form}
    #print(request.user.is_authenticated()) # at this point will be false
    if form.is_valid():
         username = form.cleaned_data.get('user')
         password = form.cleaned_data.get('password')
         print(password)
         user = authenticate(request, username=username, password=password)
         print(user)
         if user is not None and user.active:
             login(request, user)
             # return redirect('home.html')
             return HttpResponse('<h1>Logged inn</h1>')
         else:
             print('Invalid user')## show on page

    form = UserLoginForm()
    return render(request,template_name,context)

#Code to logout a user
def logout_view(request):

    template_name = 'accounts/logout.html'
    logout(request)
    return render(request,template_name,{})


#Code to logout a user
def register_view(request):
    form = RegisterForm(request.POST or None)
    template_name = 'accounts/signup.html'
    context = {'form': form}
    if form.is_valid():
        form.save()

    return render(request,template_name,context)
