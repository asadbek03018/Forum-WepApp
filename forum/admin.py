from django.contrib import admin

from .models import Forum, Category, Thread, Post
# from config.models import ForumCreators
# Register your models here.

# This line of code is importing the `Forum`, `Category`, `Thread`, and `Post` models from the
# `models.py` file in the current directory (package). These models are typically Django models that
# represent database tables and are used to define the structure and behavior of the data in the
# application. By importing these models, you can register them with the Django admin site to manage
# them through the admin interface.


# @admin.register(ForumCreators)
# class ForumCreatorsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'forum')
#     list_display_links = ('id', 'user')


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'forum_question', 'status')
    list_display_links = ('id', 'category', 'forum_question')
    search_fields = ('id', 'category', 'forum_question')
    list_per_page = 25
    list_filter = ('category', 'forum_question')
    ordering = ('id',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_select_related = ('category',)
    list_editable = ('status',)
    list_max_show_all = 100
  
admin.site.register(Category)  
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', )
#     list_display_links = ('id', 'category',)
#     search_fields = ('id', 'name',)
    
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'forum', 'title', 'creator', 'created_at', 'updated_at')
    list_display_links = ('id', 'forum', 'title')
    search_fields = ('id', 'forum', 'title')
    list_per_page = 25
    list_filter = ('forum', 'title')
    ordering = ('id',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_select_related = ('forum',)
    list_editable = ()
    list_max_show_all = 100

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'author', 'content', 'created_at', 'updated_at')
    list_display_links = ('id', 'thread', 'author')
    search_fields = ('id', 'thread', 'author')
    list_per_page = 25
    list_filter = ('thread', 'author')
    ordering = ('id',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_select_related = ('thread', 'author')
    list_editable = ()
    list_max_show_all = 100
    
