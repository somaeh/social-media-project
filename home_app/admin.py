from django.contrib import admin

from.models import UserPost, Comment


# class PostAdmin(admin.ModelAdmin):
#     List_display = ('user', 'slug', 'update')
#     search_fields = ('slug', 'body')
#     list_filter = ('update',)
#     prepopulated_fields ={'slug':('body,')}
#     raw_id_fields = ('user',)




# @admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
   
   list_display = ('user', 'slug', 'created')
   search_fields = ('slug',)
   list_filter = ('update',)
   prepopulated_fields = {'slug':('body',)}
#    raw_id_fields = ('user',)
   
   
admin.site.register(UserPost, UserPostAdmin)
class CommentAdmin(admin.ModelAdmin):
   list_display = ('user', 'post', 'created', 'is_reply')
   
admin.site.register(Comment, CommentAdmin)