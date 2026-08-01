import os
import threading
from flask import Flask
import telebot

# Достаем токен из скрытых настроек Render
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Страница для проверки работы сервера Render
@app.route('/')
def index():
    return "Сервер работает!", 200

# Пример простой команды для проверки бота
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Бот успешно запущен на Render!")

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке, чтобы он не мешал веб-серверу
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    
    # Render сам выдаст нужный порт, Flask его подхватит
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
