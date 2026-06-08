from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User

@login_required
def chat_view(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    messages = Message.objects.filter(sender__in=[request.user, receiver], receiver__in=[request.user, receiver]).order_by("timestamp")
    return render(request, "chat_room.html", {"receiver": receiver, "messages": messages})
