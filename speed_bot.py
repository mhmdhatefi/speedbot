import telebot
from telebot import types
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

users_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    users_data[user_id] = {}
    bot.send_message(user_id, "⚡️ خوش اومدی به speedbot!
لطفاً اسم کاملت رو وارد کن:")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    user_id = message.chat.id

    if user_id not in users_data or "name" not in users_data[user_id]:
        users_data[user_id]["name"] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("OpenVPN")
        bot.send_message(user_id, "محصول مورد نظرت رو انتخاب کن:", reply_markup=markup)
        return

    if "product" not in users_data[user_id]:
        if message.text not in ["OpenVPN"]:
            bot.send_message(user_id, "لطفاً یک محصول معتبر انتخاب کن.")
            return
        users_data[user_id]["product"] = message.text
        bot.send_message(user_id, "چه تعدادی می‌خوای؟")
        return

    if "quantity" not in users_data[user_id]:
        if not message.text.isdigit():
            bot.send_message(user_id, "لطفاً فقط عدد وارد کن.")
            return
        users_data[user_id]["quantity"] = int(message.text)
        total = users_data[user_id]["quantity"] * 110000
        users_data[user_id]["total"] = total
        bot.send_message(user_id, f"💰 مبلغ قابل پرداخت: {total:,} تومان
لطفاً عکس رسید پرداختی رو ارسال کن.")
        return

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.chat.id
    photo_id = message.photo[-1].file_id
    caption = f"""📩 فیش واریزی از طرف کاربر: {user_id}
🧾 نام: {users_data[user_id].get("name")}
📦 محصول: {users_data[user_id].get("product")}
🔢 تعداد: {users_data[user_id].get("quantity")}
💰 مبلغ: {users_data[user_id].get("total"):,} تومان"""

    admin_id = os.getenv("ADMIN_ID")
    bot.send_photo(admin_id, photo_id, caption=caption)
    bot.send_message(user_id, "✅ رسیدت ارسال شد و بعد از تأیید، فایل برات ارسال می‌شه.")

bot.polling()
