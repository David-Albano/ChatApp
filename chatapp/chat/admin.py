from django.contrib import admin
from chat.models import ChatUsers, ChatMessages, Conversations

# Register your models here.
admin.site.register(ChatUsers)
admin.site.register(ChatMessages)
admin.site.register(Conversations)
