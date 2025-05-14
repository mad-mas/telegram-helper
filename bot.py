import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackContext, Update
import logging

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

# تنظیمات اولیه برای ثبت لاگ‌ها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# هندلر برای مدیریت خطاها
def error(update: Update, context: CallbackContext):
    logger.warning(f"Update {update} caused error {context.error}")

# ساخت اپلیکیشن با توکن
application = Application.builder().token(TOKEN).build()

# اینجا می‌توانید دستورات و هندلرهای ربات را اضافه کنید

# ثبت هندلر خطا
application.add_error_handler(error)

# شروع ربات
application.run_polling()
