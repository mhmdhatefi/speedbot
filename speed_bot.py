import telebot

# توکن واقعی رباتت رو اینجا بذار
TOKEN = "7930430070:AAH8BFS7KtRdJQvXnpN9FwY8JBYy5TDfkyI"
bot = telebot.TeleBot(TOKEN)

# ذخیره‌سازی اطلاعات کاربران
user_data = {}

# شروع گفتگو
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    bot.send_message(user_id, "⚡️ خوش اومدی به speedbot!

لطفاً اسم کاملت رو وارد کن:")

# دریافت نام
@bot.message_handler(func=lambda msg: user_data.get(msg.chat.id) and "name" not in user_data[msg.chat.id])
def get_name(message):
    user_id = message.chat.id
    user_data[user_id]["name"] = message.text.strip()
    bot.send_message(user_id, "🛍 لطفاً محصول مورد نظرت رو انتخاب کن:

فقط یک گزینه موجوده:
1. OpenVPN - تک کاربره - نامحدود - قیمت: ۱۱۰ هزار تومان")

# دریافت تعداد
@bot.message_handler(func=lambda msg: user_data.get(msg.chat.id) and "name" in user_data[msg.chat.id] and "count" not in user_data[msg.chat.id])
def get_quantity(message):
    user_id = message.chat.id
    try:
        count = int(message.text.strip())
        user_data[user_id]["count"] = count
        total = 110000 * count
        bot.send_message(user_id, f"💰 مبلغ قابل پرداخت: {total:,} تومان

لطفاً فیش واریزی رو به صورت عکس ارسال کن.")
    except ValueError:
        bot.send_message(user_id, "❌ لطفاً تعداد را به صورت عدد وارد کن.")

# دریافت فیش پرداختی
@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    user_id = message.chat.id
    file_id = message.photo[-1].file_id
    bot.send_message(user_id, "✅ فیش با موفقیت دریافت شد. منتظر تأیید ادمین باش.")
    admin_id = "ADMIN_ID"
    bot.send_photo(admin_id, file_id, caption=f"💳 فیش جدید از طرف {user_data.get(user_id, {}).get('name', 'کاربر')} 
UserID: {user_id}")

bot.polling()
