import os
import json
import subprocess
import threading
from flask import Flask
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# --- 1. خادم ويب مصغر لإبقاء الخدمة مجانية على Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "SwingX Bot is running 24/7 Free!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# تشغيل خادم الويب في الخلفية
threading.Thread(target=run_flask, daemon=True).start()

# --- 2. كود البوت الأصلي ---
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8883664398:AAE_qBpUM9a8PzeVZ3p4VDP7fmAjxGwP_ks")
bot = telebot.TeleBot(TOKEN)

def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🔍 فحص السوق"),
        KeyboardButton("💥 أسهم انفجارية"),
        KeyboardButton("📊 الصفقات الحالية"),
        KeyboardButton("📈 الاختبار التاريخي (Backtest)")
    )
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **مرحباً بك في SwingX Bot!**\n\n"
        "مساعدك الذكي لتتبع استراتيجية سوينغ الزخم، الاختراقات، والدورات الزمنية.\n\n"
        "اختر إحدى المهام من القائمة أدناه للبدء:"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text

    if "فحص السوق" in text or text == "/scan":
        bot.send_message(chat_id, "🔍 **[SwingX]** جاري تشغيل فحص السوق اليومي وتحليل المتوسطات...")
        try:
            result = subprocess.run(["python", "run_once.py", "scan"], capture_output=True, text=True, timeout=300)
            output = result.stdout if result.stdout else "تم تشغيل الفحص بنجاح."
            bot.send_message(chat_id, f"✅ **اكتمل فحص السوق:**\n```\n{output[:3500]}\n```", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(chat_id, f"❌ حدث خطأ أثناء تشغيل الفحص: {e}")

    elif "أسهم انفجارية" in text or text == "/explosive":
        bot.send_message(chat_id, "💥 **[SwingX]** جاري البحث عن الأسهم الانفجارية والرخيصة ذات السيولة العالية...")
        try:
            result = subprocess.run(["python", "run_once.py", "explosive"], capture_output=True, text=True, timeout=300)
            output = result.stdout if result.stdout else "تم البحث."
            bot.send_message(chat_id, f"📊 **نتائج الأسهم الانفجارية:**\n```\n{output[:3500]}\n```", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(chat_id, f"❌ حدث خطأ: {e}")

    elif "الصفقات الحالية" in text or text == "/positions":
        if os.path.exists("positions.json"):
            try:
                with open("positions.json", "r", encoding="utf-8") as f:
                    positions = json.load(f)
                
                if not positions:
                    bot.send_message(chat_id, "📂 لا توجد صفقات مفتوحة حالياً في `positions.json`.")
                else:
                    msg = "📋 **الصفقات المفتوحة حالياً:**\n\n"
                    for pos in positions:
                        msg += f"• **{pos.get('symbol')}**: دخول عند ${pos.get('entry_price')} | وقف: ${pos.get('stop_loss')} \vert{} هدف: ${pos.get('target')}\n"
                    bot.send_message(chat_id, msg, parse_mode="Markdown")
            except Exception as e:
                bot.send_message(chat_id, f"⚠️ خطأ في قراءة ملف الصفقات: {e}")
        else:
            bot.send_message(chat_id, "📂 ملف الصفقات `positions.json` غير موجود بعد.")

    elif "الاختبار التاريخي" in text or text == "/backtest":
        bot.send_message(chat_id, "📈 **[SwingX]** جاري تشغيل الاختبار التاريخي الاستراتيجي (`backtest_full.py`)... قد يستغرق هذا دقيقة.")
        try:
            result = subprocess.run(["python", "backtest_full.py"], capture_output=True, text=True, timeout=600)
            output = result.stdout if result.stdout else "تم تنفيذ الاختبار."
            bot.send_message(chat_id, f"📊 **نتائج Backtest:**\n```\n{output[:3800]}\n```", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(chat_id, f"❌ حدث خطأ أثناء تشغيل الاختبار التاريخي: {e}")

if __name__ == "__main__":
    print("🚀 SwingX Bot is running...")
    bot.infinity_polling()
