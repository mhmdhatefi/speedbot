import telebot
from telebot import types
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("TOKEN")  # دریافت توکن از محیط اجرا
ADMIN_ID = 7312897446
PRODUCT_PRICE = 110000

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    bot.send_message(user_id, "⚡️ خوش اومدی speed ربات", reply_markup=None)
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.chat.id
    user_data[user_id]['name'] = message.text.strip()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("OpenVPN")
    bot.send_message(user_id, "🎯 محصول مورد نظر خود را انتخاب کنید:", reply_markup=markup)
    bot.register_next_step_handler(message, get_product)

# ادامه کدهای رباتت این پایین می‌تونه باشه...
