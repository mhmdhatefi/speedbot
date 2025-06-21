import telebot
from telebot import types
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    bot.send_message(user_id, "⚡️ خوش اومدی به speedbot!")

    msg = bot.send_message(user_id, "👤 لطفاً نام خود را وارد کنید:")
    bot.register_next_step_handler(msg, process_name)

def process_name(message):
    user_id = message.chat.id
    user_data[user_id]['name'] = message.text

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("OpenVPN")
    msg = bot.send_message(user_id, "🛍 لطفاً محصول مورد نظر را انتخاب کنید:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_product)

def process_product(message):
    user_id = message.chat.id
    user_data[user_id]['product'] = message.text

    msg = bot.send_message(user_id, "🔢 تعداد مورد نیاز را وارد کنید:")
    bot.register_next_step_handler(msg, process_quantity)

def process_quantity(message):
    user_id = message.chat.id
    try:
        quantity = int(message.text)
        total = quantity * 110000
        user_data[user_id]['quantity'] = quantity
        user_data[user_id]['total'] = total
        bot.send_message(user_id, f"💰 مبلغ قابل پرداخت: {total:,} تومان")
        msg = bot.send_message(user_id, "🧾 لطفاً فیش واریزی را ارسال کنید:")
        bot.register_next_step_handler(msg, handle_receipt)
    except ValueError:
        msg = bot.send_message(user_id, "❌ لطفاً یک عدد معتبر وارد کنید:")
        bot.register_next_step_handler(msg, process_quantity)

def handle_receipt(message):
    user_id = message.chat.id
    if message.photo:
        admin_id = os.getenv("ADMIN_ID")
        caption = f"📩 فیش واریزی از طرف کاربر:

👤 نام: {user_data[user_id]['name']}
📦 محصول: {user_data[user_id]['product']}
🔢 تعداد: {user_data[user_id]['quantity']}
💳 مبلغ: {user_data[user_id]['total']:,} تومان"
        bot.send_photo(admin_id, message.photo[-1].file_id, caption=caption)
        bot.send_message(user_id, "✅ فیش شما با موفقیت ارسال شد. منتظر تایید ادمین بمانید.")
    else:
        msg = bot.send_message(user_id, "❌ لطفاً تصویر فیش را ارسال کنید:")
        bot.register_next_step_handler(msg, handle_receipt)

bot.infinity_polling()