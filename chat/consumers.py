import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User
from .models import ChatRoom, Message, DirectMessage
from channels.db import database_sync_to_async


# مصرف کننده وب سوکت برای اتاق چت
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']  # دریافت کاربر از scope
        self.room_name = self.scope['url_route']['kwargs']['room_name']  # دریافت نام اتاق از URL
        self.room_group_name = 'chat_%s' % self.room_name  # نام گروه برای کانال لایه

        if not self.user.is_authenticated:  # بررسی احراز هویت کاربر
            await self.close()  # بستن اتصال در صورت عدم احراز هویت
            return

        # بررسی عضویت کاربر در اتاق چت
        is_member = await self.check_membership(self.room_name, self.user)
        if not is_member:
            await self.close()  # بستن اتصال در صورت عدم عضویت
            return

        # اضافه کردن کانال به گروه
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  # پذیرش اتصال

    async def disconnect(self, close_code):
        # حذف کانال از گروه
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)  # بارگذاری داده‌های JSON
        message = text_data_json['message']
        user = self.scope["user"]

        if user.is_authenticated:  # بررسی احراز هویت کاربر
            chatroom = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
            # ایجاد پیام جدید در پایگاه داده
            await database_sync_to_async(Message.objects.create)(
                chatroom=chatroom,
                user=user,
                content=message
            )

            # ارسال پیام به گروه
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # ارسال پیام به وب سوکت
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }, ensure_ascii=False))

    @database_sync_to_async
    def check_membership(self, room_name, user):
        try:
            chatroom = ChatRoom.objects.get(name=room_name)
            return user in chatroom.users.all()
        except ChatRoom.DoesNotExist:
            return False


# مصرف کننده وب سوکت برای پیام‌های مستقیم
class DirectMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if not self.user.is_authenticated:  # بررسی احراز هویت کاربر
            await self.close()
            return

        self.receiver_username = self.scope['url_route']['kwargs']['receiver_username']
        self.receiver = await database_sync_to_async(User.objects.get)(username=self.receiver_username)

        # مرتب‌سازی نام‌های کاربری برای اطمینان از نام یکتا برای گروه
        users = sorted([self.user.username, self.receiver_username])
        self.room_group_name = f'direct_{users[0]}_{users[1]}'

        # اضافه کردن کانال به گروه
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  # پذیرش اتصال

    async def disconnect(self, close_code):
        # حذف کانال از گروه
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)  # بارگذاری داده‌های JSON
        message = text_data_json['message']

        if self.user.is_authenticated:  # بررسی احراز هویت کاربر
            # ایجاد پیام مستقیم جدید در پایگاه داده
            direct_message = await database_sync_to_async(DirectMessage.objects.create)(
                sender=self.user,
                receiver=self.receiver,
                content=message
            )

            # ارسال پیام به گروه
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'direct_message',
                    'message': message,
                    'sender': self.user.username
                }
            )

    async def direct_message(self, event):
        message = event['message']
        sender = event['sender']

        # ارسال پیام به وب سوکت
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }, ensure_ascii=False))
