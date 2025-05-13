from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from keep_alive import keep_alive
keep_alive()

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['دکمه کانال', 'دکمه اطلاعات تماس'], ['دکمه پیام خودکار']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("سلام! به ربات خوش اومدی. از دکمه‌ها استفاده کن:", reply_markup=reply_markup)

async def channel_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لینک کانالhttps://t.me/+wAr7iUJGuUQxMmY0")

async def contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("@techlandhub")

async def auto_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("این یک پیام خودکار است!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex("دکمه کانال"), channel_info))
app.add_handler(MessageHandler(filters.Regex("دکمه اطلاعات تماس"), contact_info))
app.add_handler(MessageHandler(filters.Regex("دکمه پیام خودکار"), auto_message))

print("✅ ربات با موفقیت راه‌اندازی شد.")
app.run_polling()
