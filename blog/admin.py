from django.contrib import admin
from .models import Post, Comment, SearchQuery

admin.site.register(Post)
admin.site.register(SearchQuery)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')  
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')