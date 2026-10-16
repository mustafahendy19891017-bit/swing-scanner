import os
import time
import threading
from flask import Flask
import telebot

# استبدل هذا بالتوكن الخاص بك
TOKEN = '8883664398:AAE_qBpUM9a8PzeVZ3p4VDP7fmAjxGwP_ks'
bot = telebot.TeleBot(TOKEN)

# إعداد خادم Flask البسيط للحفاظ على استيقاظ البوت على Render (Web Service)
app = Flask(__name__)

@app.route('/')
def home():
    return "SwingX Bot is active and running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# دالة توليد التقرير بالتنسيق الاحترافي الذي طلبته
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

# معالجة أمر /start لعرض القائمة الرئيسية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    welcome_text = (
        "🤖 مرحباً بك في SwingX Bot!\n\n"
        "مساعدك الذكي لتتبع استراتيجية سوينغ الزخم، الاختراقات، والدورات الزمنية.\n\n"
        "اختر إحدى المهام من القائمة أدناه للبدء:"
    )
    
    # إنشاء لوحة مفاتيح أزرار تفاعلية
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton('📊 تقرير السوق اليومي')
    btn2 = telebot.types.KeyboardButton('💥 أسهم انفجارية')
    markup.add(btn1, btn2)
    
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

# الرد على الأزرار التي يضغطها المستخدم
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    if message.text == '📊 تقرير السوق اليومي':
        report = generate_market_report()
        bot.send_message(chat_id, report)
    elif message.text == '💥 أسهم انفجارية':
        bot.send_message(chat_id, "🔍 جاري مسح الأسهم الانفجارية والاختراقات الحالية...\n\n- MSFT: 540.80 | انفجار سعري (RSI: 77.8)")
    else:
        bot.send_message(chat_id, "يرجى استخدام الأزرار الموجودة في الأسفل أو كتابة /start للبدء.")

# تشغيل خادم الويب في خلفية منفصلة
if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    print("Bot is starting polling...")
    # التشغيل المستمر للبوت
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(15)
