from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet, DirectMessageViewSet, register, login, join_room

# ایجاد یک router برای API های مبتنی بر ViewSet
router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'directmessages', DirectMessageViewSet)

# تعریف urlpatterns برای مدیریت URL های API
urlpatterns = [
    path('', include(router.urls)),  # شامل کردن تمامی URL های مربوط به router
    path('register/', register, name='register'),  # URL برای ثبت نام کاربر جدید
    path('login/', login, name='login'),  # URL برای ورود کاربر
    path('join/<str:room_name>/', join_room, name='join-room'),  # URL برای عضویت کاربر در اتاق چت
]
