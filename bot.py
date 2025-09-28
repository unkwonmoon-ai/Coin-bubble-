import os
import telebot
import requests
from bs4 import BeautifulSoup

# توکن رو از Environment Variable می‌گیره
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ Bot token not found. Please set BOT_TOKEN in Render Environment Variables.")

bot = telebot.TeleBot(TOKEN)

# لیست سکه‌هایی که پشتیبانی می‌کنیم
COINS = {
    "ربع سکه": "sekebarr-rob",
    "نیم سکه": "sekebarr-nim",
    "سکه امامی": "sekebarr-emami",
    "تمام سکه بهار آزادی": "sekebarr-bahar"
}

def fetch_coin_data(coin_id):
    """داده‌ها رو از سایت tgju می‌گیره"""
    url = f"https://www.tgju.org/profile/{coin_id}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        price = soup.select_one(".price").text.strip().replace(",", "")
        intrinsic = soup.select_one(".info .value").text.strip().replace(",", "")
        price = float(price)
        intrinsic = float(intrinsic)
        bubble = price - intrinsic
        percent = (bubble / intrinsic) * 100
        return price, bubble, percent
    except Exception as e:
        print("Parse error:", e)
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "👋 سلام! خوش اومدی.\n\n"
        "لطفاً یکی از موارد زیر را تایپ کنید:\n"
        "- ربع سکه\n"
        "- نیم سکه\n"
        "- سکه امامی\n"
        "- تمام سکه بهار آزادی\n"
    )
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    coin_name = message.text.strip()
    if coin_name not in COINS:
        bot.reply_to(message, "❌ نام سکه نامعتبر است. یکی از موارد لیست را تایپ کنید.")
        return

    data = fetch_coin_data(COINS[coin_name])
    if not data:
        bot.reply_to(message, "⚠️ خطا در دریافت اطلاعات از سایت.")
        return

    price, bubble, percent = data
    reply = (
        f"📊 اطلاعات {coin_name}:\n"
        f"💰 قیمت بازار: {price:,.0f} تومان\n"
        f"📉 حباب: {bubble:,.0f} تومان\n"
        f"📈 درصد حباب: {percent:.2f}%"
    )
    bot.reply_to(message, reply)

print("🤖 Bot is running...")
bot.infinity_polling()
