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
from.models import Relation






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
    
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        
        return super().setup(request, *args, **kwargs)
    
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
                if self.next:
                    
                    return redirect(self.next)
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
        is_following = False
        user = User.objects.get(id=user_id)
        # posts = UserPost.objects.filter(user=user)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, self.template_name, {'user': user, 'posts': posts, 'is_following':is_following})
    
    
    
class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
       user = User.objects.get(pk=kwargs['user_id'])
       relation = Relation.objects.filter(from_user=request.user, to_user=user)
       if relation.exists():
           messages.error(request, 'this user already following', extra_tags='danger')
       else:
           Relation.objects.create(from_user=request.user, to_user=user)
           messages.success(request, 'you folloed this user', extra_tags='success')
       return redirect('account_app:profile', user.id)
    
    
    
class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['post_id'])
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user ', extra_tags='success')
        else:
            messages.error(request, 'you are not following this user', extra_tags='danger')
            return redirect('account_app:profile', user.id)
    
        
        
        

        
    
        
        
            