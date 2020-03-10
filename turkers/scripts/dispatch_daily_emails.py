from users.models import User
from chats.models import Chat

from django.conf import settings
from django.core.mail import send_mail


def num_new_messages_in_chat(user, chat):
    last_message = chat.messages.filter(sender=user).first()
    if last_message:
        return chat.messages.filter(timestamp__gt=last_message.timestamp).count()
    else:
        return chat.messages.count()


def run():
    turkers_chat = Chat.objects.get_collective_chat()
    for turker in User.objects.turkers():
        private_messages = num_new_messages_in_chat(turker, turker.chat)
        turkers_messages = num_new_messages_in_chat(turker, turkers_chat)

        email_content = f"""
Hi {turker.username},

You have {private_messages} in you private chat and {turkers_messages} messages in the turkers chat since your last interactions.

Click in the link bellow to go to the website and reply to the new messages:

https://turkers.aarea.co/

Thanks,
Exchange w/Turkers
""".strip()

        print(email_content)

        send_mail(
            'Your daily report from Exchange w/ Turkers',
            email_content,
            settings.DEFAULT_FROM_EMAIL,
            ['bernardoxhc@gmail.com'],
        )
