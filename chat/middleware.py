from django.conf import settings
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser, User
from urllib.parse import parse_qs


# تابع غیرهمزمان برای دریافت کاربر از توکن
@database_sync_to_async
def get_user(token):
    try:
        # بررسی و تایید صحت توکن JWT
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        # بازگرداندن کاربر مربوطه
        return User.objects.get(id=user_id)
    except:
        # در صورت بروز خطا، بازگرداندن کاربر ناشناس
        return AnonymousUser()


# Middleware برای احراز هویت JWT
class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # تجزیه query string برای استخراج توکن
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        # تنظیم کاربر در scope
        scope['user'] = await get_user(token)
        # ادامه پردازش با فراخوانی متد والد
        return await super().__call__(scope, receive, send)
