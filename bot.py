import telebot
import requests

TOKEN = "8902169965:AAF2lXAWtCkZ7UuewPD5XPIGNKxvLqjRDD4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Baga nagaan dhufte! Gaaffii kee barreessi, ani deebii siif nan kenna.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # As keessatti Key hin barbaadu
    try:
        # Hojii kee as keessatti bifa salphaan hojjeta
        bot.reply_to(message, "Botiin kee ammallee hojjetaa jira! Key si hin dhiba.")
    except Exception as e:
        bot.reply_to(message, "Rakkoo uumameera.")

bot.polling()
