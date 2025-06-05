from django.contrib import admin
from .models import UserMessage



@admin.register(UserMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject', 'body')


