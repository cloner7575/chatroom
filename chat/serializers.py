from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatRoom, Message, DirectMessage


# Serializer برای مدل User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # فیلدهایی که در خروجی JSON گنجانده می‌شوند


# Serializer برای مدل ChatRoom
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'users']  # فیلدهایی که در خروجی JSON گنجانده می‌شوند


# Serializer برای مدل Message
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'user', 'content', 'timestamp']  # فیلدهایی که در خروجی JSON گنجانده می‌شوند


# Serializer برای مدل DirectMessage
class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']  # فیلدهایی که در خروجی JSON گنجانده می‌شوند
