from re import search
from django.contrib import admin
from.models import Post ,comment,QuillPost
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display =("title" , "author" , "slug" , "status" ,"publish")
    list_filter = ("publish","status")
    search_fields =("title" , "body")

@admin.register(comment)
class CommentAdmin(admin.ModelAdmin):
    list_display =["name","email","post","active"]
    list_filter =("active","created")
    search_fields =("name","email","body")
    

@admin.register(QuillPost)
class QuillPostAdmin(admin.ModelAdmin):
    pass