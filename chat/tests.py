from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import ChatRoom, Message


# تست‌های مربوط به کاربران
class UserTests(APITestCase):
    # تست ثبت نام کاربر
    def test_register_user(self):
        url = reverse('register')  # URL مربوط به ثبت نام
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')  # ارسال درخواست POST برای ثبت نام
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # بررسی کد وضعیت
        self.assertIn('access', response.data)  # بررسی وجود توکن دسترسی در پاسخ
        self.assertIn('refresh', response.data)  # بررسی وجود توکن تازه‌سازی در پاسخ

    # تست ورود کاربر
    def test_login_user(self):
        User.objects.create_user(username='testuser', password='testpassword')  # ایجاد کاربر
        url = reverse('login')  # URL مربوط به ورود
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')  # ارسال درخواست POST برای ورود
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # بررسی کد وضعیت
        self.assertIn('access', response.data)  # بررسی وجود توکن دسترسی در پاسخ
        self.assertIn('refresh', response.data)  # بررسی وجود توکن تازه‌سازی در پاسخ


# تست‌های مربوط به اتاق‌های چت
class ChatRoomTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')  # ایجاد کاربر
        self.client.force_authenticate(user=self.user)  # احراز هویت کاربر

    # تست ایجاد اتاق چت
    def test_create_chatroom(self):
        url = reverse('chatroom-list')  # URL مربوط به لیست اتاق‌های چت
        data = {
            'name': 'TestRoom',
            'users': [self.user.id]
        }
        response = self.client.post(url, data, format='json')  # ارسال درخواست POST برای ایجاد اتاق چت
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # بررسی کد وضعیت
        self.assertEqual(ChatRoom.objects.count(), 1)  # بررسی تعداد اتاق‌های چت ایجاد شده
        self.assertEqual(ChatRoom.objects.get().name, 'TestRoom')  # بررسی نام اتاق چت ایجاد شده

    # تست عضویت در اتاق چت
    def test_join_chatroom(self):
        chatroom = ChatRoom.objects.create(name='TestRoom')  # ایجاد اتاق چت
        url = reverse('join-room', kwargs={'room_name': chatroom.name})  # URL مربوط به عضویت در اتاق چت
        response = self.client.post(url, format='json')  # ارسال درخواست POST برای عضویت در اتاق چت
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # بررسی کد وضعیت
        self.assertIn(self.user, chatroom.users.all())  # بررسی عضویت کاربر در اتاق چت


# تست‌های مربوط به پیام‌ها
class MessageTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')  # ایجاد کاربر
        self.client.force_authenticate(user=self.user)  # احراز هویت کاربر
        self.chatroom = ChatRoom.objects.create(name='TestRoom')  # ایجاد اتاق چت
        self.chatroom.users.add(self.user)  # اضافه کردن کاربر به اتاق چت

    # تست ارسال پیام
    def test_send_message(self):
        url = reverse('message-list')  # URL مربوط به لیست پیام‌ها
        data = {
            'chatroom': self.chatroom.id,
            'user': self.user.id,
            'content': 'Hello, this is a test message.'
        }
        response = self.client.post(url, data, format='json')  # ارسال درخواست POST برای ارسال پیام
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # بررسی کد وضعیت
        self.assertEqual(Message.objects.count(), 1)  # بررسی تعداد پیام‌های ایجاد شده
        self.assertEqual(Message.objects.get().content, 'Hello, this is a test message.')  # بررسی محتوای پیام ایجاد شده
