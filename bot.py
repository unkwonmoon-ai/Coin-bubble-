import os
import telebot
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")  # دریافت توکن از Environment Variable
bot = telebot.TeleBot(BOT_TOKEN)

# لیست نام‌های سکه و آدرس‌های مربوطه در سایت tgju.org
COINS = {
    "ربع سکه": "sekebarr-rob",
    "نیم سکه": "sekebarr-nim",
    "سکه امامی": "sekebarr-emami",
    "تمام سکه بهار آزادی": "sekebarr-tamam"
}

def fetch_coin_data(coin_url):
    url = f"https://www.tgju.org/profile/{coin_url}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        price_element = soup.select_one(".price")
        intrinsic_value_element = soup.select_one(".info .value")

        if not price_element or not intrinsic_value_element:
            return None, None, None

        price = int(price_element.text.strip().replace(",", ""))
        intrinsic_value = int(intrinsic_value_element.text.strip().replace(",", ""))
        bubble = price - intrinsic_value
        bubble_percent = (bubble / intrinsic_value) * 100

        return price, bubble, bubble_percent

    except Exception as e:
        print(f"خطا در دریافت اطلاعات: {e}")
        return None, None, None

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     "سلام 🌸\nلطفا یکی از موارد زیر را تایپ کنید:\nربع سکه\nنیم سکه\nسکه امامی\nتمام سکه بهار آزادی")

@bot.message_handler(func=lambda msg: True)
def send_coin_info(message):
    coin_name = message.text.strip()
    if coin_name in COINS:
        price, bubble, bubble_percent = fetch_coin_data(COINS[coin_name])
        if price:
            bot.send_message(message.chat.id,
                             f"💰 قیمت بازار {coin_name}: {price:,} تومان\n"
                             f"📈 حباب: {bubble:,} تومان\n"
                             f"📊 درصد حباب: {bubble_percent:.2f}%")
        else:
            bot.send_message(message.chat.id, "خطا در دریافت اطلاعات از سایت.")
    else:
        bot.send_message(message.chat.id, "لطفا یکی از موارد مشخص شده را وارد کنید.")

if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.infinity_polling()
