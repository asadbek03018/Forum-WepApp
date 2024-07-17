from django.contrib import admin
from .models import ForumCreators

# Register your models here.
@admin.register(ForumCreators)
class ForumCreatorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'forum')
    list_display_links = ('id', 'user')