import telebot
from telebot import types

TOKEN = '7785880031:AAHXamJroQ6FDGdU0vVKPE-Vtd_GkdlVHOo'
bot = telebot.TeleBot(TOKEN)

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💅 کاشت ناخن")
    btn2 = types.KeyboardButton("🌸 ترمیم ناخن")
    btn3 = types.KeyboardButton("🎨 طراحی ناخن")
    btn4 = types.KeyboardButton("✨ ژلیش")
    btn5 = types.KeyboardButton("📅 نوبت‌های من")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(
        message.chat.id,
        "سلام عزیز دل 🌸\nبه سامانه نوبت‌دهی *Samira Nail Art* خوش اومدی!\n\n"
        "لطفاً یکی از خدمات زیر رو انتخاب کن:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# پاسخ به انتخاب خدمات
@bot.message_handler(func=lambda m: True)
def handle_services(message):
    service = message.text
    if service in ["💅 کاشت ناخن", "🌸 ترمیم ناخن", "🎨 طراحی ناخن", "✨ ژلیش"]:
        bot.reply_to(message, f"✅ {service} انتخاب شد.\n\nلطفاً تاریخ و ساعت مورد نظر رو بنویس.")
    elif service == "📅 نوبت‌های من":
        bot.reply_to(message, "⏳ این بخش در دست توسعه است.")
    else:
        bot.reply_to(message, "❌ لطفاً یکی از گزینه‌های منو رو انتخاب کن.")

bot.polling()
