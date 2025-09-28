import telebot
import requests
from bs4 import BeautifulSoup
import os

# دریافت توکن ربات از متغیر محیطی
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# URL صفحه وب TGJU برای اطلاعات حباب سکه‌ها
url = 'https://english.tgju.org/profile/crypto-bubble-imaginaryones/performance'

# دریافت اطلاعات حباب سکه‌ها از صفحه وب
def get_coin_bubble():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # استخراج اطلاعات حباب سکه‌ها از محتوای HTML
    bubble_data = soup.find('div', {'class': 'performance'})
    return bubble_data.text.strip()

# دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من ربات حباب سکه هستم. برای دریافت اطلاعات حباب سکه‌ها، دستور /bubble را وارد کنید.")

# دستور /bubble
@bot.message_handler(commands=['bubble'])
def send_bubble(message):
    bubble = get_coin_bubble()
    bot.reply_to(message, f"اطلاعات حباب سکه‌ها:\n{bubble}")

# شروع ربات
bot.polling()
