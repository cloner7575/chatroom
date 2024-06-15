from django.urls import re_path
from . import consumers

# الگوهای URL برای WebSocket
websocket_urlpatterns = [
    # URL برای اتاق چت
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # URL برای پیام‌های مستقیم
    re_path(r'ws/direct/(?P<receiver_username>\w+)/$', consumers.DirectMessageConsumer.as_asgi()),
]
