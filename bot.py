import telebot
import requests
from bs4 import BeautifulSoup

# توکن ربات رو اینجا بذار
BOT_TOKEN = "توکن_خودت_اینجا"

bot = telebot.TeleBot(BOT_TOKEN)

# تابع برای گرفتن قیمت و حباب
def get_gold_data():
    url = "https://www.tgju.org/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # داده‌ها رو بر اساس id از سایت می‌گیریم
    items = {
        "ربع سکه": "sekee-rob",
        "نیم سکه": "sekee-nim",
        "سکه امامی": "sekeb",
        "تمام سکه بهار آزادی": "sekee-bahar"
    }

    result = {}
    for name, item_id in items.items():
        try:
            parent = soup.find("tr", {"id": item_id})
            price_text = parent.find("td", {"class": "nf"}).text.strip().replace(",", "")
            bubble_text = parent.find_all("td")[-1].text.strip().replace(",", "")

            price = int(price_text)
            bubble = int(bubble_text)

            # درصد حباب = (حباب / قیمت واقعی) * 100
            percent = round((bubble / (price - bubble)) * 100, 2) if price > bubble else 0

            result[name] = {
                "price": price,
                "bubble": bubble,
                "percent": percent
            }
        except Exception:
            result[name] = {"error": "خطا در دریافت داده"}

    return result

# دستور /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "سلام 👋\nنام یکی از سکه‌ها (ربع سکه، نیم سکه، سکه امامی، تمام سکه بهار آزادی) رو بفرست تا قیمت و حباب رو بهت بگم.")

# پردازش پیام کاربر
@bot.message_handler(func=lambda msg: True)
def reply_price(message):
    user_text = message.text.strip()
    data = get_gold_data()

    if user_text in data:
        info = data[user_text]
        if "error" in info:
            bot.reply_to(message, f"⚠️ {info['error']}")
        else:
            response = (
                f"💰 {user_text}\n"
                f"قیمت: {info['price']:,} تومان\n"
                f"حباب: {info['bubble']:,} تومان\n"
                f"درصد حباب: {info['percent']}%"
            )
            bot.reply_to(message, response)
    else:
        bot.reply_to(message, "❌ لطفاً یکی از گزینه‌ها رو بفرست:\nربع سکه، نیم سکه، سکه امامی، تمام سکه بهار آزادی")

print("Bot is running...")
bot.infinity_polling()
