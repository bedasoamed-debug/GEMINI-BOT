import telebot
from telebot import types
import google.generativeai as genai
import threading
import os
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

TOKEN = "8902169965:AAF2lXAWtCkZ7UuewPD5XPIGNKxvLqjRDD4"
bot = telebot.TeleBot(TOKEN)

# Key kee isa suuraa 1000043907.jpg irraa argatte qulqulleessitee galchi
GEMINI_API_KEY = "AQ.Ab8RN6JwTpxhgNm2llwy_Dc8RHRuz..." # As irratti key kee isa guutuu galchi
genai.configure(api_key=GEMINI_API_KEY)

LOGO_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80" 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Baga Nagaan Dhufte! Kun GEMINI BOT dha.**\n\n"
        "Gemini Bot AI ammayyaa dandeettii dacha qabu yoo ta'u, "
        "kallattiin Google Gemini SDK tekinolojiitiin siif hojjeta!\n\n"
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
    
    try:
        # SDK haaraa kanaan modelii waamna
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_query)
        ai_response = response.text
    except Exception as e:
        ai_response = f"❌ Dogoggora SDK uumameera: {str(e)}\nMee koodii kee irratti pip install google-generativeai mirkaneessi."

    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=waiting_msg.message_id, text=ai_response)
    except Exception as e:
        bot.send_message(message.chat.id, ai_response)

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    print("GEMINI BOT hojii eegaleera...")
    bot.infinity_polling()
