import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from datetime import datetime, timedelta
from config import BOT_TOKEN, ADMIN_ID, CHANNEL_USERNAME

bot = telebot.TeleBot(BOT_TOKEN)

with open("services.json", encoding="utf-8") as f:
    services = json.load(f)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    for srv in services:
        markup.add(InlineKeyboardButton(text=srv["name"], callback_data=f"service_{srv['name']}"))
    markup.add(InlineKeyboardButton("تأیید انتخاب", callback_data="confirm_services"))
    user_data[message.chat.id] = {"services": []}
    bot.send_message(message.chat.id, "سلام! لطفاً خدمات مورد نظر را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def select_service(call):
    service = call.data.split("_", 1)[1]
    if service not in user_data[call.message.chat.id]["services"]:
        user_data[call.message.chat.id]["services"].append(service)
        bot.answer_callback_query(call.id, f"{service} اضافه شد")
    else:
        bot.answer_callback_query(call.id, f"{service} قبلاً انتخاب شده")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_services")
def confirm_services(call):
    selected = user_data[call.message.chat.id]["services"]
    if not selected:
        bot.answer_callback_query(call.id, "هیچ خدمتی انتخاب نشده")
        return
    user_data[call.message.chat.id]["date"] = None
    days_markup = InlineKeyboardMarkup()
    weekdays = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
    for i in range(6):
        day = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        days_markup.add(InlineKeyboardButton(f"{weekdays[i % 6]} - {day}", callback_data=f"date_{day}"))
    bot.edit_message_text("تاریخ نوبت را انتخاب کنید:", call.message.chat.id, call.message.message_id, reply_markup=days_markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("date_"))
def select_date(call):
    date = call.data.split("_", 1)[1]
    user_data[call.message.chat.id]["date"] = date
    times_markup = InlineKeyboardMarkup()
    for h in range(10, 19):
        times_markup.add(InlineKeyboardButton(f"{h}:00", callback_data=f"time_{h}"))
    bot.edit_message_text("ساعت مورد نظر را انتخاب کنید:", call.message.chat.id, call.message.message_id, reply_markup=times_markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("time_"))
def select_time(call):
    hour = call.data.split("_", 1)[1]
    user_info = user_data[call.message.chat.id]
    services_list = "\n".join(user_info["services"])
    date = user_info["date"]
    summary = f"🔔 نوبت شما ثبت شد:\n📅 تاریخ: {date}\n🕘 ساعت: {hour}:00\n💅 خدمات:\n{services_list}"
    bot.send_message(call.message.chat.id, summary)
    bot.send_message(ADMIN_ID, f"کاربر @{call.from_user.username or call.from_user.first_name}\n{summary}")
    bot.answer_callback_query(call.id, "نوبت ثبت شد. ممنون 🌸")

@bot.message_handler(commands=['نمونه_کار'])
def show_samples(message):
    bot.send_message(message.chat.id, f"📸 برای دیدن نمونه‌کارها وارد کانال زیر شوید:
👉 https://t.me/{CHANNEL_USERNAME}")

bot.infinity_polling()
