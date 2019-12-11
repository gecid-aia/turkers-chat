from django.contrib import admin

from chats.models import Chat, Message


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    has_add_permission = lambda self, request: False
    readonly_fields = ['turker']
    list_display = ['title', 'info']


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message)
