from telegram import Update
from telegram.ext import ContextTypes

# شروع ربات برای کاربران
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات فروش ووچر و خدمات وان ایکس بت هستم. از من استفاده کنید.")

# پردازش پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"پیام شما: {update.message.text}")
