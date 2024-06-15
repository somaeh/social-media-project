from django import forms

from.models import UserPost, Comment





class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        
        model = UserPost
        fields = ('body',)
        
        
        
class CommentCretaeForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets ={
            'body': forms.Textarea(attrs={'class':'form-control', 'style': 'max-width: 400px;'})
        }
        
class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets ={
            'body': forms.Textarea(attrs={'class':'form-control', 'style': 'max-width: 400px;'})
        }
        
class PostSearchForm(forms.Form):
    
    search=forms.CharField()
        