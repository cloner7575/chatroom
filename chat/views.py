from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ChatRoom, Message, DirectMessage
from .serializers import UserSerializer, ChatRoomSerializer, MessageSerializer, DirectMessageSerializer

# ثبت نام کاربر جدید
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(serializer.errors)

# ورود کاربر
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'detail': 'اطلاعات ورود نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)

# ViewSet برای مدیریت اتاق‌های چت
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

# ViewSet برای مدیریت پیام‌ها
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

# ViewSet برای مدیریت پیام‌های مستقیم
class DirectMessageViewSet(viewsets.ModelViewSet):
    queryset = DirectMessage.objects.all()
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # بازگرداندن پیام‌های ارسالی و دریافتی کاربر
        return DirectMessage.objects.filter(sender=user) | DirectMessage.objects.filter(receiver=user)

# عضویت کاربر در اتاق چت
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_room(request, room_name):
    user = request.user
    chatroom = get_object_or_404(ChatRoom, name=room_name)
    chatroom.users.add(user)
    chatroom.save()
    return Response({'detail': f'{user.username} به اتاق {room_name} اضافه شد'}, status=status.HTTP_200_OK)
