import os
import requests
from flask import Flask, request
import telebot

TOKEN = os.environ.get('TELEGRAM_TOKEN') or os.environ.get('BOT_TOKEN') or "8761851210:AAGL39MaJj68VAMo4wv0SWxUcvsLtQXQK3M"
AI_KEY = os.environ.get('AI_KEY') or "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"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def ask_openrouter(user_message):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {AI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        if response.status_code == 200:
            return response.json()['choices']['message']['content']
        return f"Ошибка API: {response.status_code}"
    except Exception as e:
        return f"Ошибка связи с ИИ: {str(e)}"

@app.route('/', methods=['GET'])
def index():
    return "Сервер активен!", 200

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Бот на вебхуках готов к работе!")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    ai_response = ask_openrouter(message.text)
    bot.reply_to(message, ai_response)

if __name__ == "__main__":
    bot.remove_webhook()
    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
    if RENDER_URL:
        bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
