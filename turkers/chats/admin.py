from django.contrib import admin

from chats.models import Chat, Message


def block_op(self, request):
    return False


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    has_add_permission = block_op
    readonly_fields = ["turker"]
    list_display = ["title", "info"]


class MessageAdmin(admin.ModelAdmin):
    search_fields = ['content', 'sender__username']
    list_filter = ['chat']
    model = Message
    has_add_permission = block_op
    readonly_fields = ['chat', 'sender', 'content', 'timestamp', 'reply_to']
    list_display = ['content', 'sender', 'chat']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('sender', 'chat')


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
