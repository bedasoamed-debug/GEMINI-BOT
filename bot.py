import telebot
from telebot import types
import requests
import threading
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

TOKEN = "8902169965:AAF2lXAWtCkZ7UuewPD5XPIGNKxvLqjRDD4"
bot = telebot.TeleBot(TOKEN)

GEMINI_API_KEY = "AQ.Ab8RN6LRb-YbH3Sj3SKkNYdrYu6zXdIhT_G9aI3M6C2RRZRvug"

LOGO_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80" 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Baga Nagaan Dhufte! Kun GEMINI BOT dha.**\n\n"
        "Gemini Bot AI ammayyaa dandeettii dacha qabu yoo ta'u, "
        "kallattiin Google Gemini REST API tekinolojiitiin siif hojjeta!\n\n"
        "👇 Filannoowwan armaan gadii cuqaasii fayyadami, ykn gaaffii kee barreessi!"
    )
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("📝 Choose Model")
    btn2 = types.KeyboardButton("🎨 Image Generation")
    btn3 = types.KeyboardButton("🔍 Web Search")
    btn4 = types.KeyboardButton("🎬 Video Generation")
    btn5 = types.KeyboardButton("📄 File Recognition")
    btn6 = types.KeyboardButton("🎸 Music Generation")
    btn7 = types.KeyboardButton("🚀 Premium")
    btn8 = types.KeyboardButton("👤 My Account")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    
    try:
        bot.send_photo(message.chat.id, LOGO_URL, caption=welcome_text, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text
    
    if user_query in ["📝 Choose Model", "🎨 Image Generation", "🔍 Web Search", "🎬 Video Generation", "📄 File Recognition", "🎸 Music Generation", "🚀 Premium", "👤 My Account"]:
        bot.reply_to(message, f"✨ Hojii **{user_query}** jedhu filattanii jirtu. Dandeettiin kun dabalataan hojjetamaa jira!", parse_mode="Markdown")
        return

    waiting_msg = bot.reply_to(message, "🧠 *Gemini Bot AI deebii kee xiinxalaa jira...*", parse_mode="Markdown")
    
    api_url = api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": user_query}]}]}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=25)
        if response.status_code == 200:
            res_data = response.json()
            ai_response = res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            ai_response = "⚠️ Server Error: Mee sarara kee irra deebii qulqulleessi."
    except Exception as e:
        ai_response = "❌ Hanqinni network uumameera. Irra deebii yaali."

    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=waiting_msg.message_id, text=ai_response)
    except Exception as e:
        bot.send_message(message.chat.id, ai_response)

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    print("GEMINI BOT hojii eegaleera...")
    bot.infinity_polling()
