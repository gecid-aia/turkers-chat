from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def chats_index(request):
    return render(request, "chats/index.html")
