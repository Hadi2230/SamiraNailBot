import telebot
from telebot import types

TOKEN = '7785880031:AAGRt7NIit9BwUcXlBk4aqfl09a8Of5SfH0'
CHANNEL_USERNAME = '@SamiraNailArtGallery'  # نام کانال نمونه کار (حتما @ داشته باشه)
bot = telebot.TeleBot(TOKEN)

user_data = {}

# استارت اولیه
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("✅ شروع"))
    bot.send_message(
        message.chat.id,
        f"سلام {message.from_user.first_name} عزیز 🌸\n"
        "به سامانه نوبت‌دهی *Samira Nail Art* خوش اومدی!\n\n"
        "برای شروع، لطفاً دکمه «✅ شروع» رو بزن.",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# منوی اصلی بعد از "شروع"
@bot.message_handler(func=lambda m: m.text == "✅ شروع")
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📅 نوبت‌های من", "🖼 نمونه کار", "📞 ارتباط با من")
    bot.send_message(message.chat.id, "از منوی زیر یکی رو انتخاب کن 👇", reply_markup=markup)

# نمایش نمونه کارها از کانال
@bot.message_handler(func=lambda m: m.text == "🖼 نمونه کار")
def samples(message):
    try:
        posts = bot.get_chat_history(CHANNEL_USERNAME, limit=5)  # ۵ پست آخر کانال (اگر محدودیت داشت کمش کن)
    except Exception as e:
        bot.send_message(message.chat.id, "متأسفانه دسترسی به نمونه کارها مقدور نیست.")
        return

    # ارسال عکس‌های هر پست
    sent_any = False
    for post in posts:
        if post.content_type == 'photo':
            bot.send_photo(message.chat.id, post.photo[-1].file_id)
            sent_any = True

    if not sent_any:
        bot.send_message
