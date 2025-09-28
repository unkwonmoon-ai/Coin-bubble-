import telebot
import requests
from bs4 import BeautifulSoup
import os

# دریافت توکن ربات از متغیر محیطی
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# URL صفحه سکه‌ها در سایت zcoinn
URL = "https://zcoinn.com/coin/"

# نگهداری نام سکه‌ها و شناسه‌های آن‌ها
coins = {
    "ربع سکه": "ربع-سکه",
    "نیم سکه": "نیم-سکه",
    "سکه امامی": "سکه-امامی",
    "تمام سکه بهار آزادی": "تمام-سکه-بهار-آزادی",
}

# تابع دریافت اطلاعات از سایت zcoinn
def get_coin_info(coin_name):
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # پیدا کردن بخش مربوط به هر سکه
        coin_div = soup.find("a", {"href": f"/coin/{coins[coin_name]}"})
        if not coin_div:
            return None

        parent = coin_div.find_parent("tr")
        cells = parent.find_all("td")

        price_text = cells[2].text.strip()  # قیمت فروش
        bubble_text = cells[3].text.strip()  # حباب

        price_num = float(price_text.replace(",", ""))
        bubble_num = float(bubble_text.replace(",", ""))

        intrinsic_value = price_num - bubble_num
        percent_bubble = (bubble_num / intrinsic_value) * 100
        percent_bubble = round(percent_bubble, 2)

        return price_text, bubble_text, percent_bubble

    except Exception as e:
        return None

# دستور /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "سلام 🌸\nلطفاً یکی از سکه‌ها را وارد کنید:\nربع سکه\nنیم سکه\nسکه امامی\nتمام سکه بهار آزادی",
    )

# پاسخ به پیام‌ها
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    coin = message.text.strip()
    if coin not in coins:
        bot.reply_to(message, "سکه یافت نشد ❌ لطفاً یکی از موارد پیشنهادی را وارد کنید.")
        return

    result = get_coin_info(coin)
    if result:
        price, bubble, percent_bubble = result
        bot.reply_to(
            message,
            f"💰 قیمت {coin}: {price} تومان\n📈 حباب: {bubble} تومان\n📊 درصد حباب: {percent_bubble}%",
        )
    else:
        bot.reply_to(message, "خطا در دریافت اطلاعات از سایت 😔 لطفاً بعداً امتحان کنید.")

# اجرای ربات
bot.polling()
