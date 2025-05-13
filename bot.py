import os
from dotenv import load_dotenv
from telegram.ext import Application

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# گرفتن توکن و ایدی از متغیرهای محیطی
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# چک کردن اگر توکن یا ایدی موجود نیست
if not TOKEN:
    raise ValueError("Bot token is missing!")
if not ADMIN_ID:
    raise ValueError("Admin ID is missing!")

# ساخت اپلیکیشن با توکن
application = Application.builder().token(TOKEN).build()

# در اینجا می‌توانید دستورات و هندلرهای ربات را اضافه کنید
# ...

# شروع ربات
application.run_polling()
