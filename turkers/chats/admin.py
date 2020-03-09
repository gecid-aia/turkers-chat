from django.contrib import admin

from chats.models import Chat, Message


def block_op(self, request):
    return False


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    has_add_permission = block_op
    readonly_fields = ["turker"]
    list_display = ["title", "info"]


class MessagesWithProfanityFilter(admin.SimpleListFilter):
    title = 'Messages with swear words'
    parameter_name = 'profanity'

    def lookups(self, request, model_admin):
        return (
            ('', 'All messages'),
            ('swear', 'With swear words'),
            ('no_swear', 'Without swear words'),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == 'swear':
            return queryset.filter(content__icontains='***')
        elif value == 'no_swear':
            return queryset.exclude(content__icontains='***')


class MessageAdmin(admin.ModelAdmin):
    search_fields = ['content', 'sender__username']
    list_filter = ['chat', MessagesWithProfanityFilter]
    model = Message
    has_add_permission = block_op
    readonly_fields = ['chat', 'sender', 'content', 'timestamp', 'reply_to']
    list_display = ['content', 'sender', 'chat']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('sender', 'chat')


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
