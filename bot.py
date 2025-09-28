import os
import telebot

TOKEN = os.environ.get("BOT_TOKEN")  # توکن رو بعداً توی Render میذاری
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام 👋 لطفاً اول مقدار حباب و بعد قیمت سکه را وارد کنید.\n\nفرمت: حباب,قیمت")

@bot.message_handler(func=lambda m: True)
def calculate(message):
    try:
        data = message.text.replace(" ", "").split(",")
        bubble = int(data[0])
        price = int(data[1])
        intrinsic = price - bubble
        percent = (bubble / intrinsic) * 100
        reply = f"""📊 نتیجه محاسبه:
- قیمت بازار: {price:,} تومان
- مقدار حباب: {bubble:,} تومان
- ارزش ذاتی: {intrinsic:,} تومان
- درصد حباب ≈ {percent:.2f}%"""
    except Exception:
        reply = "❌ لطفاً مقدارها را به‌درستی وارد کنید.\nمثال: 7707000,25160000"
    bot.reply_to(message, reply)

print("Bot is running...")
bot.infinity_polling()
