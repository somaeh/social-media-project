from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import UserPost
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib import messages
from.forms import PostCreateUpdateForm
from django.utils.text import slugify
class HomeView(View):
    def get(self, request):
        posts=UserPost.objects.all()  
        return render(request, 'home_app/home.html', {'posts': posts})
    
class PostDetailView(View):
    
    def get(self, request, post_id, post_slug):
        
        post = UserPost.objects.get(pk=post_id, slug=post_slug)
        comments = post.pcomments.filter(is_reply=False)  #کامنت اصلی یعنی کامنت پدر است 
        return render(request, 'home_app/postdetail.html', {'post':post, 'comments':comments})
    
class PostDeleteView(LoginRequiredMixin, View):
    
    def get(self, request, post_id):
        post = UserPost.objects.get(id=post_id)
        
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post delete successfully', extra_tags='success')
        else:
            messages.error(request, 'you cant delete this post', extra_tags='danger')
        return redirect('home_app:home')
class PostUpdateView(LoginRequiredMixin, View):
    
    form_class = PostCreateUpdateForm
    def setup(self, request, *args, **kwargs): 
        self.post_instance = UserPost.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "you cant update this post ", extra_tags='danger')
            return redirect('home_app:home')
        
        return super().dispatch(request, *args, **kwargs)
        
     
    def get(self, request, *args, **kwargs):
        post=self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home_app/update.html', {'form':form})
        
        
    def post(self, request, *args, **kwargs):
        
       post=self.post_instance
       form = self.form_class(request.POST, initial=post)
       if form.is_valid():
            new_post=form.save(commit=False) #
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'update successfully', extra_tags='success')
            return redirect('home_app:postdetail', post.id, post.slug)
        
        
        
class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'home_app/create.html', {'form': form})
    def post(self, request, *args, **kwargs):
        
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug=slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'create a new post successfully', extra_tags='success')
            return redirect('home_app:post_detail', new_post.id, new_post.slug)
     
    
            
        
    
        

        

    
    
    





