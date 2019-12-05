from django.contrib import admin

from chats.models import Chat


class ChatAdmin(admin.ModelAdmin):
    model = Chat


admin.site.register(Chat, ChatAdmin)
