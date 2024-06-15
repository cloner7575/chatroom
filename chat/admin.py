from django.contrib import admin
from .models import DirectMessage, Message, ChatRoom


# ثبت مدل DirectMessage در پنل مدیریت Django
@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content')  # فیلدهایی که در لیست نمایش داده می‌شوند


# ثبت مدل Message در پنل مدیریت Django
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chatroom', 'user', 'content', 'timestamp')  # فیلدهایی که در لیست نمایش داده می‌شوند


# ثبت مدل ChatRoom در پنل مدیریت Django
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name',)  # فیلدهایی که در لیست نمایش داده می‌شوند
