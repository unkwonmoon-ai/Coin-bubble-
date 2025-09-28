import telebot
import requests
from bs4 import BeautifulSoup
import os

# دریافت توکن ربات از متغیر محیطی
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# URL صفحه وب TGJU برای اطلاعات حباب سکه‌ها
url = 'https://www.tgju.org/profile/coin'

# نگهداری نام سکه‌ها و URL یا بخش مرتبط در سایت TGJU
coin_paths = {
    "ربع سکه": "rab-sekeh",
    "نیم سکه": "nim-sekeh",
    "سکه امامی": "emami-sekeh",
    "تمام سکه بهار آزادی": "bahar-azadi",
}

# دریافت اطلاعات حباب سکه از سایت
def get_coin_info(coin):
    if coin not in coin_paths:
        return None

    try:
        response = requests.get(f"{url}/{coin_paths[coin]}")
        soup = BeautifulSoup(response.text, "html.parser")

        # پیدا کردن قیمت بازار
        price_tag = soup.find("div", {"class": "price"})
        price = price_tag.text.strip() if price_tag else "نامشخص"

        # پیدا کردن حباب
        bubble_tag = soup.find("div", {"class": "bubble"})
        bubble = bubble_tag.text.strip() if bubble_tag else "نامشخص"

        # محاسبه درصد حباب
        if price != "نامشخص" and bubble != "نامشخص":
            price_num = float(price.replace(",", ""))
            bubble_num = float(bubble.replace(",", ""))
            intrinsic_value = price_num - bubble_num
            percent_bubble = (bubble_num / intrinsic_value) * 100
            percent_bubble = round(percent_bubble, 2)
        else:
            percent_bubble = "نامشخص"

        return price, bubble, percent_bubble

    except Exception as e:
        return None

# دستور /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "سلام 🌸\nنام یکی از سکه‌ها را وارد کنید:\nربع سکه\nنیم سکه\nسکه امامی\nتمام سکه بهار آزادی",
    )

# پاسخ به پیام‌ها
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    coin = message.text.strip()
    result = get_coin_info(coin)
    if result:
        price, bubble, percent_bubble = result
        bot.reply_to(
            message,
            f"💰 قیمت {coin}: {price} تومان\n📈 حباب: {bubble} تومان\n📊 درصد حباب: {percent_bubble}%",
        )
    else:
        bot.reply_to(message, "سکه یافت نشد یا مشکل در دریافت اطلاعات پیش آمد.")

# اجرای ربات
bot.polling()
