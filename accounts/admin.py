from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Message
# Register your models here.

# @admin.register(Account)
# class AccountAdmin(ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number')
#     list_filter = ('is_staff', )
#     list_editable = ('phone_number', )
#     search_fields = ('id', 'first_name', 'last_name', 'username', 'email')

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'date_joined', 'is_active')
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('id', 'first_name', 'last_name', 'username', 'email')
    ordering = ('-date_joined', )
    list_display_links = ('id', 'first_name', 'last_name')
    # Neeed else returned error
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'is_read', 'created_at')
    list_display_links = ('id', 'sender')
    list_editable = ('is_read', )
    search_fields = ('id', 'sender')
    ordering = ('-created_at', )

