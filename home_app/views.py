from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import UserPost, Comment, Vote
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib import messages
from.forms import PostCreateUpdateForm, CommentCretaeForm, CommentReplyForm, PostSearchForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify









class HomeView(View):
    
    form_class=PostSearchForm
    
    
    def get(self, request):
        posts=UserPost.objects.all()  
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home_app/home.html', {'posts':posts, 'form':self.form_class})
    
# class PostDetailView(View):
#     # form_class = CommentCretaeForm
#     form_class_reply = CommentReplyForm
    
    
    
#     def setup(self, request, *args, **kwargs): 
#         self.post_instance = UserPost.objects.get(pk=kwargs['post_id'], slug=kwargs['post_slug'])
#         return super().setup(request, *args, **kwargs)
    
#     def get(self, request,  *args, **kwargs):
        
#         post = UserPost.objects.get(pk=kwargs['post_id'], slug=kwargs['post_slug'])
#         comments = self.post_instance.pcomments.filter(is_reply=False)  #کامنت اصلی یعنی کامنت پدر است 
#         return render(request, 'home_app/postdetail.html', {'post':self.post_instance, 'comments':comments, 'form':self.form_class, 'reply_form':self.form_class_reply})
    
#     @method_decorator(login_required)
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.user = request.user
#             new_comment_post = self.post_instance
#             new_comment.save()
#             messages.success(request, "your comment comitedd successfully", extra_tags='success')
#             return redirect('home_app:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDetailView(View):
    form_class=CommentCretaeForm
    form_class_reply=CommentReplyForm
    
    def setup(self, request, *args, **kwargs): 
        self.post_instance = get_object_or_404(UserPost, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply=False)  # کامنت اصلی یعنی کامنت پدر است 
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        return render(request, 'home_app/postdetail.html', {
            'post':self.post_instance, 
            'comments':comments, 
            'form':self.form_class, 
            'reply_form':self.form_class_reply,
            'can_like':can_like
        })
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # reply_form = self.form_class_reply(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "نظر شما با موفقیت ارسال شد", extra_tags='success')
            return redirect('home_app:post_detail', self.post_instance.id, self.post_instance.slug)
        # اگر فرم نامعتبر باشد، مجدداً قالب را با فرم و پیام‌های خطا رندر کنید
        comments = self.post_instance.pcomments.filter(is_reply=False)
        return render(request, 'home_app/postdetail.html', {
            'post': self.post_instance, 
            'comments': comments, 
            'form': form, 
            'reply_form': self.form_class_reply()
        })
            
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
        
        
        
        
class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm
    
    def post(self, request, post_id, comment_id):
        post = get_object_or_404(UserPost, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, "جواب با موفقیت ارسال شد", extra_tags='success')
        return redirect('home_app:post_detail', post.id, post.slug)
    
    
class PostLikeView(LoginRequiredMixin, View):
    
    def get(self, request, post_id):
        
        post = get_object_or_404(UserPost, id=post_id)
        likes = Vote.objects.filter(post=post, user=request.user)
        if likes.exists():
            messages.error(request, 'این پست قبلا لایک شده است', extra_tags='danger')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'پست لایک شدبا موفقیت', extra_tags='success')
        return redirect('home_app:post_detail', post.id, post.slug)
     
    
            
        
    
        

        

    
    
    





