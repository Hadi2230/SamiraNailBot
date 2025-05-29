import telebot
from datetime import datetime

TOKEN = '7785880031:AAHXamJroQ6FDGdU0vVKPE-Vtd_GkdlVHOo'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """سلام عزیز دل 🌸 به سامانه نوبت‌دهی Samira Nail Art خوش اومدی!
لطفاً نوع خدمات و زمان مورد نظرت رو انتخاب کن 💅""")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "ممنون از پیامت ❤️ این بخش هنوز در حال توسعه‌ست.")

bot.polling()
