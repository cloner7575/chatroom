from django.db import models
from django.contrib.auth.models import User


# مدل برای اتاق چت
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)  # نام اتاق چت
    users = models.ManyToManyField(User, related_name='chatrooms')  # کاربران عضو اتاق چت

    def __str__(self):
        return self.name  # نمایش نام اتاق چت به عنوان نمایشی از شیء


# مدل برای پیام‌ها در اتاق چت
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)  # اتاق چت مرتبط با پیام
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # کاربر ارسال کننده پیام
    content = models.TextField()  # محتوای پیام
    timestamp = models.DateTimeField(auto_now_add=True)  # زمان ارسال پیام

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'  # نمایش کاربر و قسمتی از محتوای پیام به عنوان نمایشی از شیء


# مدل برای پیام‌های مستقیم بین کاربران
class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)  # کاربر ارسال کننده پیام
    receiver = models.ForeignKey(User, related_name='received_messages',
                                 on_delete=models.CASCADE)  # کاربر دریافت کننده پیام
    content = models.TextField()  # محتوای پیام
    timestamp = models.DateTimeField(auto_now_add=True)  # زمان ارسال پیام

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}: {self.content[:20]}'  # نمایش ارسال کننده، گیرنده و قسمتی از محتوای پیام به عنوان نمایشی از شیء
