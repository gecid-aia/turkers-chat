from chats.models import Chat


def parse_msg(msg):
    timestamp = msg.timestamp.strftime('%x %X')
    content = f'[{msg.sender.username} - {timestamp}]\n{msg.content}'
    if msg.reply_to:
        msg = msg.reply_to
        timestamp = msg.timestamp.strftime('%x %X')
        content += f'\nREPLY TO: [{msg.sender.username} - {timestamp}] - {msg.content}'
    return content


def run():
    """
    Run as:

    $ python turkers/manage.py runscript messages_as_txt
    """
    for chat in Chat.objects.all():
        messages = []
        for msg in chat.messages.select_related('sender', 'reply_to').order_by('timestamp'):
            messages.append(parse_msg(msg))

        filename = f'{chat.title}.txt'.replace(' ', '_').lower()
        with open(filename, 'w') as fd:
            fd.write('\n\n'.join(messages))
