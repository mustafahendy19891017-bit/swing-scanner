import os
import time
import threading
from flask import Flask
import telebot

TOKEN = '8883664398:AAE_qBpUM9a8PzeVZ3p4VDP7fmAjxGwP_ks'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "SwingX Bot is active and running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# دالة توليد التقرير بالتنسيق الذي طلبته
def generate_market_report():
    report = """🚀 تقرير المسح المتقدم - 📈 تداول سوينغ (Swing - Daily)
-----------------------------------

📌 الأسهم الأمريكية:
- MSFT
🔹 السعر الحالي / الشراء: 540.01
🎯 هدف البيع المقترح: 615.23
🛑 وقف الخسارة المقترح: 502.40
📊 مؤشر RSI: 77.5
-------------------------
💱 الفوركس (GBPJPY):
BUY NOW

Entry: 208.670
SL: 208.100
TP1: 208.830
TP2: 209.250
TP3: 209.600"""
    return report

# دالة مساعدة لإنشاء لوحة المفاتيح بشكل دائم
def get_main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton('📊 تقرير السوق اليومي')
    btn2 = telebot.types.KeyboardButton('💥 أسهم انفجارية')
    markup.add(btn1, btn2)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    welcome_text = (
        "🤖 مرحباً بك في SwingX Bot!\n\n"
        "مساعدك الذكي لتتبع استراتيجية سوينغ الزخم، الاختراقات، والدورات الزمنية.\n\n"
        "اختر إحدى المهام من القائمة أدناه للبدء:"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text
    
    if text == '📊 تقرير السوق اليومي':
        report = generate_market_report()
        bot.send_message(chat_id, report, reply_markup=get_main_keyboard())
    elif text == '💥 أسهم انفجارية':
        explosive_text = "🔍 جاري مسح الأسهم الانفجارية والاختراقات الحالية...\n\n- MSFT: 540.80 | انفجار سعري (RSI: 77.8)"
        bot.send_message(chat_id, explosive_text, reply_markup=get_main_keyboard())
    else:
        bot.send_message(chat_id, "يرجى استخدام الأزرار الموجودة في الأسفل:", reply_markup=get_main_keyboard())

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    print("Bot is starting polling...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(15)
