import os
from flask import Flask, request
import telebot

# Берем токен из настроек Render
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Страница-заглушка для Render
@app.route('/', methods=['GET'])
def index():
    return "Сервер активен!", 200

# Маршрут, куда Telegram будет присылать сообщения
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# Единственная рабочая команда (для проверки)
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Теперь я официально работаю через Webhook на Render!")

if __name__ == "__main__":
    # Удаляем старый вебхук и ставим новый на адрес вашего приложения
    bot.remove_webhook()
    
    # Render автоматически подставит имя вашего сервиса в переменную RENDER_EXTERNAL_URL
    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
    if RENDER_URL:
        bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    
    # Запуск сервера на порту Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

