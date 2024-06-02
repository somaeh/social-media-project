from django.shortcuts import render
from django.views import View
from .models import UserPost


class HomeView(View):
    def get(self, request):
        posts=UserPost.objects.all()
        return render(request, 'home_app/home.html', {'posts': posts})
    
class PostDetailView(View):
    
    def get(self, request, post_id, post_slug):
        
        post = UserPost.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'home_app/postdetail.html', {'post':post})
    
    
    





