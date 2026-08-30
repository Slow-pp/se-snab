import os
import telebot
from google import genai

# Railway автоматически подтянет ключи из переменных окружения
GEMINI_API_KEY = os.getenv("AQ.Ab8RN6IVcoNasbwQe7bxI6PCCoQTbTrvZvB06jhBhksIplp6aw")
TELEGRAM_BOT_TOKEN = os.getenv("8793461738:AAFNPGqOgXfh1pNH5qMkuhdAqw0_YC5XPdQ")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "Привет! Я ваш бот по снабжению, запущенный в облаке Railway. Чем могу помочь?"
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка при обращении к ИИ: {e}")

if __name__ == "__main__":
    print("Бот запущен в облаке и ожидает сообщения...")
    bot.infinity_polling()