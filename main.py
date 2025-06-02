import telebot
from telebot import types

TOKEN = '7785880031:AAGRt7NIit9BwUcXlBk4aqfl09a8Of5SfH0'
bot = telebot.TeleBot(TOKEN)

# ساخت حافظه ساده برای ذخیره اطلاعات کاربران (فعلاً داخل رم)
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

# مدیریت منو
@bot.message_handler(func=lambda m: m.text == "📅 نوبت‌های من")
def choose_service(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💅 کاشت ناخن", "🌸 ترمیم ناخن", "🎨 طراحی ناخن", "✨ ژلیش")
    user_data[message.chat.id] = {"step": "select_service"}
    bot.send_message(message.chat.id, "کدوم خدمات رو می‌خوای انجام بدی؟", reply_markup=markup)

# انتخاب خدمات
@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get("step") == "select_service")
def confirm_service(message):
    service = message.text
    if service not in ["💅 کاشت ناخن", "🌸 ترمیم ناخن", "🎨 طراحی ناخن", "✨ ژلیش"]:
        bot.reply_to(message, "❌ لطفاً یکی از گزینه‌های خدمات رو انتخاب کن.")
        return

    user_data[m.chat.id]["service"] = service
    user_data[m.chat.id]["step"] = "confirm_service"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✅ تایید", "❌ تغییر خدمات")
    bot.send_message(message.chat.id, f"شما انتخاب کردید: {service}\nتایید می‌کنی؟", reply_markup=markup)

# تایید خدمات یا بازگشت
@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get("step") == "confirm_service")
def service_confirm(message):
    if message.text == "✅ تایید":
        user_data[m.chat.id]["step"] = "select_date"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📅 فردا", "📅 پس‌فردا", "📅 سه‌شنبه")  # تستی، بعداً تقویم واقعی می‌ذاریم
        bot.send_message(message.chat.id, "تاریخ مورد نظر رو انتخاب کن:", reply_markup=markup)

    elif message.text == "❌ تغییر خدمات":
        user_data[m.chat.id]["step"] = "select_service"
        choose_service(message)
    else:
        bot.reply_to(message, "❌ لطفاً تایید یا تغییر خدمات رو انتخاب کن.")

# انتخاب روز (تست)
@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get("step") == "select_date")
def select_time(message):
    user_data[m.chat.id]["date"] = message.text
    user_data[m.chat.id]["step"] = "select_time"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🕙 10:00", "🕚 11:00", "🕛 12:00", "🕓 16:00", "🕖 18:00")
    bot.send_message(message.chat.id, f"تاریخ انتخاب‌شده: {message.text}\nحالا ساعت رو انتخاب کن:", reply_markup=markup)

# انتخاب ساعت و پایان
@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get("step") == "select_time")
def confirm_appointment(message):
    time = message.text
    service = user_data[m.chat.id]["service"]
    date = user_data[m.chat.id]["date"]

    bot.send_message(
        message.chat.id,
        f"📌 نوبت شما ثبت شد:\n"
        f"🔹 خدمات: {service}\n"
        f"🔹 تاریخ: {date}\n"
        f"🔹 ساعت: {time}\n\n"
        "❤️ مرسی که ما رو انتخاب کردی!\n"
        "🎁 شما ۱۰ امتیاز گرفتی 🌟"
    )
    user_data[m.chat.id] = {}  # پاک‌سازی وضعیت

# نمونه کار و ارتباط با من
@bot.message_handler(func=lambda m: m.text == "🖼 نمونه کار")
def samples(message):
    bot.send_message(message.chat.id, "🔜 بزودی نمونه‌کارها اینجا قرار می‌گیرن.")

@bot.message_handler(func=lambda m: m.text == "📞 ارتباط با من")
def contact(message):
    bot.send_message(message.chat.id, "برای هماهنگی مستقیم، به آیدی ادمین پیام بده: @EncryptedHadi")

bot.polling()
