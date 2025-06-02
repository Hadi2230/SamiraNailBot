import telebot
from telebot import types

TOKEN = '7785880031:AAHXamJroQ6FDGdU0vVKPE-Vtd_GkdlVHOo'
bot = telebot.TeleBot(TOKEN)

user_state = {}  # ذخیره وضعیت کاربر {user_id: مرحله}

services = ["💅 کاشت ناخن", "🌸 ترمیم ناخن", "🎨 طراحی ناخن", "✨ ژلیش"]

# منوی اصلی
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📅 نوبت‌های من", "🖼 نمونه کار", "📞 ارتباط با من")
    return markup

# منوی خدمات
def services_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for service in services:
        markup.add(service)
    return markup

# مرحله 1: استارت و منوی اصلی
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_state[message.chat.id] = 'main_menu'
    bot.send_message(
        message.chat.id,
        "سلام عزیز دل 🌸\nبه سامانه نوبت‌دهی *Samira Nail Art* خوش اومدی!\n\n"
        "از منوی پایین برای گرفتن نوبت اقدام کن.",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# هندلر کلی برای پیام‌ها
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text
    
    state = user_state.get(user_id, 'main_menu')
    
    if state == 'main_menu':
        if text == "📅 نوبت‌های من":
            user_state[user_id] = 'choose_service'
            bot.send_message(user_id, "لطفاً یکی از خدمات زیر رو انتخاب کن:", reply_markup=services_menu())
        elif text == "🖼 نمونه کار":
            bot.send_message(user_id, "نمونه کارها به زودی اضافه می‌شود.")
        elif text == "📞 ارتباط با من":
            bot.send_message(user_id, "برای ارتباط با ادمین این شماره را استفاده کنید: 0912xxxxxxx")
        else:
            bot.send_message(user_id, "لطفاً یکی از گزینه‌های منو رو انتخاب کن.", reply_markup=main_menu())

    elif state == 'choose_service':
        if text in services:
            user_state[user_id] = 'confirm_service'
            user_state[f"{user_id}_service"] = text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn_yes = types.KeyboardButton("تایید ✅")
            btn_no = types.KeyboardButton("لغو ❌")
            markup.add(btn_yes, btn_no)
            bot.send_message(user_id, f"خدمت {text} انتخاب شده. تایید می‌کنی؟", reply_markup=markup)
        else:
            bot.send_message(user_id, "لطفاً یکی از خدمات را از منوی پایین انتخاب کن.", reply_markup=services_menu())

    elif state == 'confirm_service':
        if text == "تایید ✅":
            user_state[user_id] = 'choose_datetime'
            bot.send_message(user_id, "لطفاً تاریخ و ساعت مورد نظر برای نوبت را به صورت متن وارد کن.\nمثلاً: 1402/03/15 ساعت 14:00")
        elif text == "لغو ❌":
            user_state[user_id] = 'choose_service'
            bot.send_message(user_id, "خدمت انتخابی لغو شد. لطفاً مجدداً یک خدمت انتخاب کن:", reply_markup=services_menu())
        else:
            bot.send_message(user_id, "لطفاً فقط تایید یا لغو را انتخاب کن.")

    elif state == 'choose_datetime':
        datetime_text = text
        service = user_state.get(f"{user_id}_service")
        # اینجا می‌تونیم ذخیره کنیم (الان فقط پیام می‌دیم)
        bot.send_message(user_id, f"نوبت برای خدمت {service} در تاریخ و ساعت {datetime_text} ثبت شد.\nامتیاز ۱۰ به حساب شما اضافه شد.")
        user_state[user_id] = 'main_menu'
        bot.send_message(user_id, "برای ادامه می‌توانید از منوی اصلی استفاده کنید.", reply_markup=main_menu())

bot.polling()
