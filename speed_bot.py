import telebot
from telebot import types
from datetime import datetime, timedelta

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 7312897446
PRODUCT_PRICE = 110000

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    bot.send_message(user_id, "سلام به ربات speed خوش اومدی⚡️\nلطفاً ابتدا نام و نام خانوادگی خود را وارد کنید…")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.chat.id
    user_data[user_id]['name'] = message.text.strip()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("OpenVPN")
    bot.send_message(user_id, "محصول مورد نظر خود را انتخاب کنید:", reply_markup=markup)
    bot.register_next_step_handler(message, get_product)

def get_product(message):
    user_id = message.chat.id
    user_data[user_id]['product'] = message.text.strip()
    bot.send_message(user_id, "📦 محصول انتخابی: OpenVPN\n👤 نوع: تک‌کاربره\n🔄 ترافیک: نامحدود\n💰 قیمت هر اشتراک: ۱۱۰,۰۰۰ تومان\n\nلطفاً تعداد مورد نیاز را وارد کنید:")
    bot.register_next_step_handler(message, get_quantity)

def get_quantity(message):
    user_id = message.chat.id
    try:
        quantity = int(message.text.strip())
        user_data[user_id]['quantity'] = quantity
        total_price = quantity * PRODUCT_PRICE
        user_data[user_id]['price'] = total_price
        bot.send_message(user_id, f"✅ مبلغ قابل پرداخت: {total_price:,} تومان\nلطفاً فیش واریزی را به صورت عکس ارسال کنید.")
        bot.register_next_step_handler(message, get_receipt)
    except ValueError:
        bot.send_message(user_id, "عدد معتبر وارد کنید! لطفاً تعداد را وارد نمایید:")
        bot.register_next_step_handler(message, get_quantity)

def get_receipt(message):
    user_id = message.chat.id
    if not message.photo:
        bot.send_message(user_id, "لطفاً تصویر فیش واریزی را ارسال کنید.")
        bot.register_next_step_handler(message, get_receipt)
        return

    file_id = message.photo[-1].file_id
    caption = f"🧾 فیش واریزی جدید\n👤 {user_data[user_id]['name']}\n💼 محصول: OpenVPN - تک‌کاربره - نامحدود\n🔢 تعداد: {user_data[user_id]['quantity']}\n💳 مبلغ: {user_data[user_id]['price']:,} تومان\n🆔 آی‌دی: {user_id}"
    bot.send_photo(ADMIN_ID, file_id, caption=caption)
    bot.send_message(user_id, "✅ فیش شما ارسال شد و در انتظار تایید ادمین هستید. پس از تایید، فایل برای شما ارسال خواهد شد.")

@bot.message_handler(commands=['sendfile'])
def send_file(message):
    if message.chat.id != ADMIN_ID:
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        file_link = parts[2]
        expire_date = datetime.now() + timedelta(days=30)
        expire_msg = f"✅ فایل شما آماده است.\n📎 لینک: {file_link}\n⏳ اعتبار: تا تاریخ {expire_date.date()}"
        bot.send_message(user_id, expire_msg)
        bot.send_message(ADMIN_ID, "فایل برای کاربر ارسال شد.")
    except:
        bot.send_message(ADMIN_ID, "❌ دستور نادرست است. فرمت دستور:\n/sendfile [user_id] [file_link]")

@bot.message_handler(commands=['warn'])
def send_warning(message):
    if message.chat.id != ADMIN_ID:
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        warn_msg = "📢 فایل شما در حال اتمام است. لطفاً برای تمدید اقدام فرمایید."
        bot.send_message(user_id, warn_msg)
        bot.send_message(ADMIN_ID, "هشدار برای کاربر ارسال شد.")
    except:
        bot.send_message(ADMIN_ID, "❌ دستور نادرست است. فرمت دستور:\n/warn [user_id]")

bot.infinity_polling()
