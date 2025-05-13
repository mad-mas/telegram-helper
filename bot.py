import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from handlers.admin_panel import admin_conv
from handlers.user_handlers import start, handle_message
import os
from dotenv import load_dotenv

load_dotenv()

# تنظیمات Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# اطلاعات حساس
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# تابع برای شروع
async def start(update: Update, context):
    """فرمان شروع ربات"""
    await update.message.reply_text("سلام! من ربات فروش ووچر و خدمات وان ایکس بت هستم. از من استفاده کنید.")

# پردازش پیام‌ها
async def handle_message(update: Update, context):
    """برای پیام‌های ساده"""
    await update.message.reply_text(f"پیام شما: {update.message.text}")

# تابع برای اجرای ربات
def main():
    application = Application.builder().token(TOKEN).build()

    # دستورات عمومی ربات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # پنل ادمین
    application.add_handler(admin_conv)

    # اجرای ربات
    application.run_polling()

if __name__ == "__main__":
    main()
