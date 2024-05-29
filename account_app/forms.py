from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'your password'}))
    
    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('there is this email')
        
        return email
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("this username already exists")
        return username
        