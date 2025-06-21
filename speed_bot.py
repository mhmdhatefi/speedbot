import telebot

TOKEN = "توکن_خودت_اینجا"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    bot.send_message(user_id, "⚡️ خوش اومدی به speedbot!")

bot.polling()
