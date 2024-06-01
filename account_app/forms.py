from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'your email'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder':'your password'}))
    password2 = forms.CharField(label='confrim password', widget=forms.PasswordInput(attrs={'placeholder':'your password'}))
    
    
    
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
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        
        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')
        
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       