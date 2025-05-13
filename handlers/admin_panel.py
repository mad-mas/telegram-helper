from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
import json
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_ID = int(os.getenv("ADMIN_ID"))

SET_DOLLAR_RATE, = range(1)

# مسیر فایل‌های ذخیره‌سازی
RATES_FILE = "data/rates.json"
ORDERS_FILE = "data/vouchers.json"

# بررسی اینکه آیا کاربر ادمین است یا نه
def is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_ID

# نمایش منو برای ادمین
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    keyboard = [
        [InlineKeyboardButton("➕ تنظیم نرخ دلار", callback_data="set_rate")],
        [InlineKeyboardButton("✅ تایید سفارشات فروش", callback_data="verify_orders")]
    ]
    await update.message.reply_text("🔐 خوش آمدید به پنل ادمین:", reply_markup=InlineKeyboardMarkup(keyboard))

# مدیریت دکمه‌های پنل ادمین
async def handle_admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    query = update.callback_query
    await query.answer()

    if query.data == "set_rate":
        await query.edit_message_text("لطفاً نرخ روز دلار را (به تومان) ارسال کنید:")
        return SET_DOLLAR_RATE

    if query.data == "verify_orders":
        if not os.path.exists(ORDERS_FILE):
            await query.edit_message_text("هیچ سفارشی برای بررسی وجود ندارد.")
            return ConversationHandler.END

        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)

        if not orders:
            await query.edit_message_text("📭 سفارشی برای تأیید وجود ندارد.")
            return ConversationHandler.END

        for order_id, info in orders.items():
            msg = (
                f"🧾 سفارش #{order_id}\n"
                f"👤 کاربر: {info['user_id']}\n"
                f"💳 شماره کارت: {info['card']}\n"
                f"💸 مبلغ: {info['amount']} تومان\n"
                f"🔢 کد ووچر: {info['voucher']}"
            )
            keyboard = [
                [InlineKeyboardButton("تأیید و پرداخت شد", callback_data=f"confirm_{order_id}")],
                [InlineKeyboardButton("رد کردن سفارش", callback_data=f"reject_{order_id}")]
            ]
            await query.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

# دریافت نرخ دلار از ادمین
async def set_dollar_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    try:
        rate = int(update.message.text)
        with open(RATES_FILE, "w") as f:
            json.dump({"rate": rate}, f)

        await update.message.reply_text(f"✅ نرخ دلار با موفقیت به {rate} تومان تنظیم شد.")
    except:
        await update.message.reply_text("❌ لطفاً فقط عدد وارد کنید.")
    return ConversationHandler.END

# تایید یا رد کردن سفارشات
async def handle_order_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    query = update.callback_query
    await query.answer()
    action, order_id = query.data.split("_", 1)

    with open(ORDERS_FILE, "r") as f:
        orders = json.load(f)

    if order_id not in orders:
        await query.edit_message_text("❌ سفارش یافت نشد.")
        return

    if action == "confirm":
        # اینجا کد پرداخت دستی اضافه میشه
        await query.edit_message_text("✅ سفارش با موفقیت تأیید و پرداخت شد.")
    elif action == "reject":
        await query.edit_message_text("🚫 سفارش رد شد.")

    del orders[order_id]

    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f)

# conversation
admin_conv = ConversationHandler(
    entry_points=[CommandHandler("admin", admin_panel)],
    states={
        SET_DOLLAR_RATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_dollar_rate)]
    },
    fallbacks=[],
    allow_reentry=True
)
