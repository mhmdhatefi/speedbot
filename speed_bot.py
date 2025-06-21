
import os
import telebot
from telebot import types
from datetime import datetime, timedelta

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN environment variable not found")

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    bot.send_message(user_id, "⚡ خوش اومدی speed bot! سلام به ربات", reply_markup=start_markup())
    bot.register_next_step_handler(message, get_name)

def start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("OpenVPN")
    return markup

def get_name(message):
    user_id = message.chat.id
    user_data[user_id]['name'] = message.text.strip()
    bot.send_message(user_id, "✅ محصول مورد نظر خود را انتخاب کنید:", reply_markup=start_markup())
    bot.register_next_step_handler(message, get_product)

def get_product(message):
    user_id = message.chat.id
    user_data[user_id]['product'] = message.text.strip()
    bot.send_message(user_id, "📦 تعداد مورد نظر را وارد کنید:")
    bot.register_next_step_handler(message, get_quantity)

def get_quantity(message):
    user_id = message.chat.id
    try:
        quantity = int(message.text.strip())
        price = 110000
        total = quantity * price
        bot.send_message(user_id, f"💰 مبلغ قابل پرداخت: {total:,} تومان
لطفا فیش واریزی را ارسال کنید.")
    except ValueError:
        bot.send_message(user_id, "❌ لطفا فقط عدد وارد کنید.")
        bot.register_next_step_handler(message, get_quantity)

bot.polling()
