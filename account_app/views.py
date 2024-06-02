from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home_app.models import UserPost






class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account_app/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_app:home')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'you register successfully', extra_tags='success')
            os.system("cls")
            return redirect('home_app:home')
            os.system("cls")
        
        return render(request, self.template_name, {'form': form})
    
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account_app/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_app:home')
        return super().dispatch(request, *args, **kwargs)   #اگر یوزر آتینتی کیت نکرده بود اجازه بده ادامه برنامه اجرا بشه مثل گت و پست
    
    
    def get(self, request):
       form = self.form_class
       return render(request, self.template_name, {'form': form})
    def post(self, request):
        
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'login successfuly', extra_tags='success')
                return redirect('home_app:home')
            messages.error(request, 'username and password are wrong', extra_tags='warning')
        return render(request, self.template_name, {'form': form})
    
class UserLogoutView(LoginRequiredMixin, View):
    # login_url = 'account_app:login'
    
    
    def get(self, request):
        logout(request)
        messages.success(request, 'user logout sccessfully', extra_tags='success')
        
        return redirect('home_app:home')
    
    
class UserProfileView(LoginRequiredMixin, View):
    template_name = 'account_app/profile.html'
    
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = UserPost.objects.filter(user=user)
        return render(request, self.template_name, {'user': user, 'posts': posts})
    
        
        
        

        
    
        
        
            