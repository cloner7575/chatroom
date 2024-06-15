# پروژه چت زنده با استفاده از Django و WebSocket

این پروژه یک برنامه چت زنده است که با استفاده از Django Rest Framework (DRF) برای بک‌اند و Django Channels برای ارتباط
زمان واقعی پیاده‌سازی شده است. این برنامه به طور کامل از زبان فارسی پشتیبانی می‌کند و شامل قابلیت‌های ایجاد چت روم،
پیوستن به چت های موجود و ارسال پیام به دیگر کاربران به صورت ریل تایم می‌باشد.

## ویژگی‌ها

- ثبت نام و ورود کاربران
- ایجاد و پیوستن به چت روم
- ارسال و دریافت پیام به صورت ریل تایم
- ارسال پیام‌ دایرکت بین کاربران

## پیش‌نیازها

- Python 3.7+
- Django 3.x
- Channels 3.x
- Daphne 3.x
- Django Rest Framework
- djangorestframework-simplejwt

## نصب

pip install -r requirements.txt


## اندپوینت‌ها

- ثبت نام کاربر جدید

  URL: /api/register/

  روش: POST

  توضیح: این اندپوینت برای ثبت نام کاربران جدید استفاده می‌شود.

ورودی:

      {
      "username": "testuser",
      "password": "testpassword",
      "email": "testuser@example.com"
      }

خروجی موفق:

    {
    "refresh": "refresh_token",
    "access": "access_token"
    }

- ورود کاربر

  URL: /api/login/

  روش: POST

  توضیح: این اندپوینت برای ورود کاربران و دریافت توکن‌های احراز هویت استفاده می‌شود.

ورودی:

    {
    "username": "testuser",
    "password": "testpassword"
    }

خروجی موفق:

    {
    "refresh": "refresh_token",
    "access": "access_token"
    }

- لیست اتاق‌های چت

  URL: /api/chatrooms/

  روش: GET

  توضیح: این اندپوینت برای دریافت لیست تمامی اتاق‌های چت استفاده می‌شود.

خروجی موفق:

    [
      
      {
        "id": 1,
        "name": "Room1",
        "users": [1, 2]
      },
      {
        "id": 2,
        "name": "Room2",
        "users": [1, 3]
      }
    ]

- ایجاد اتاق چت جدید

  URL: /api/chatrooms/

  روش: POST

  توضیح: این اندپوینت برای ایجاد یک اتاق چت جدید استفاده می‌شود.

ورودی:

      {
      "name": "NewRoom",
      "users": [1, 2]
      }

خروجی موفق:

    {
    "id": 3,
    "name": "NewRoom",
    "users": [1, 2]
    }

- ارسال پیام به اتاق چت

  URL: /api/messages/

  روش: POST

  توضیح: این اندپوینت برای ارسال پیام به اتاق چت استفاده می‌شود

ورودی:

      {
      "chatroom": 1,
      "user": 1,
      "content": "Hello, this is a test message."
      }

خروجی موفق:

      {
      "id": 1,
      "chatroom": 1,
      "user": 1,
      "content": "Hello, this is a test message.",
      "timestamp": "2023-06-14T12:34:56.789Z"
      }

## استفاده از وب سوکت

برای اتصال به WebSocket، از ابزارهایی مانند wscat یا Postman استفاده کنید. به عنوان مثال:

    wscat -c ws://localhost:8000/ws/chat/room_name/?token=your_jwt_token

- ارسال پیام

  برای ارسال پیام یک پیام به فرمت زیر به وب سوکت ارسال کنید

      {
          "message": "سلام، این یک پیام تستی است."
      }
