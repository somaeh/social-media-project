from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
import os

class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account_app/register.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'you register successfully', extra_tags='success')
            os.system("cls")
            return redirect('home_app:home')
            os.system("cls")
        
        return render(request, self.template_name, {'form': form})
            