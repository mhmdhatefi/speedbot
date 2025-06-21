import telebot
from telebot import types
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 7312897446
PRODUCT_PRICE = 110000

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    bot.send_message(user_id, "⚡ خوش اومدی به speedbot!
سلام به ربات 😎")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.chat.id
    user_data[user_id]['name'] = message.text.strip()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("OpenVPN")
    bot.send_message(user_id, "🎯 محصول مورد نظر خود را انتخاب کنید:", reply_markup=markup)
    bot.register_next_step_handler(message, get_product)

def get_product(message):
    user_id = message.chat.id
    user_data[user_id]['product'] = message.text.strip()
    bot.send_message(user_id, "📦 لطفاً تعداد را وارد کنید:")
    bot.register_next_step_handler(message, get_quantity)

def get_quantity(message):
    user_id = message.chat.id
    try:
        quantity = int(message.text.strip())
        user_data[user_id]['quantity'] = quantity
        total = quantity * PRODUCT_PRICE
        bot.send_message(user_id, f"💰 مبلغ قابل پرداخت: {total:,} تومان")
        bot.send_message(user_id, "📤 لطفاً رسید پرداخت را به صورت عکس ارسال کنید:")
        bot.register_next_step_handler(message, get_receipt)
    except ValueError:
        bot.send_message(user_id, "❗ لطفاً فقط عدد وارد کنید.")
        bot.register_next_step_handler(message, get_quantity)

def get_receipt(message):
    user_id = message.chat.id
    if message.photo:
        file_id = message.photo[-1].file_id
        bot.send_message(ADMIN_ID, f"✅ سفارش جدید از طرف: {user_data[user_id]['name']}")
        bot.send_message(ADMIN_ID, f"🎯 محصول: {user_data[user_id]['product']}
🔢 تعداد: {user_data[user_id]['quantity']}")
        bot.forward_message(ADMIN_ID, user_id, message.message_id)
        bot.send_message(user_id, "✅ رسید شما برای ادمین ارسال شد، پس از تایید فایل دریافت می‌کنید.")
    else:
        bot.send_message(user_id, "❗ لطفاً یک عکس معتبر ارسال کنید.")
        bot.register_next_step_handler(message, get_receipt)

bot.polling()