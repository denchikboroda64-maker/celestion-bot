import os
import requests
from flask import Flask, request
import telebot

# 1. ВСТАВЬТЕ СЮДА ВАШ ТОКЕН ОТ BOTFATHER ВНУТРЬ КАВЫЧЕК
TOKEN = "СЮДА_ВСТАВЬТЕ_ТОКЕН_БОТА_ОТ_BOTFATHER"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

AI_URL = "https://openrouter.ai"

# 2. ВСТАВЬТЕ СЮДА ВАШ КЛЮЧ ОТ OPENROUTER (начинается на sk-or-v1-...) ВНУТРЬ КАВЫЧЕК
AI_KEY = "СЮДА_ВСТАВЬТЕ_КЛЮЧ_ОТ_OPENROUTER"

@app.route('/', methods=['GET'])
def index():
    return "Нейросеть активна!", 200

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        if json_string:
            update = telebot.types.Update.de_json(json_string)
            if update and update.update_id:
                bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я Celestion — твой ИИ-ассистент DeepSeek. Спроси меня о чём угодно!")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_text = message.text
    
    if message.chat.type != 'private':
        if not (f"@{bot.get_me().username}" in user_text or (message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id)):
            return

    bot.send_chat_action(message.chat.id, 'typing')

    try:
        headers = {
            "Authorization": f"Bearer {AI_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek/deepseek-r1-distill-llama-8b:free",
            "messages": [{"role": "user", "content": user_text}]
        }
        
        response = requests.post(AI_URL, headers=headers, json=data, timeout=30)
        res_json = response.json()
        ai_response = res_json['choices']['message']['content']
        
    except Exception as e:
        ai_response = "Извините, нейросеть сейчас перегружена запросами. Попробуйте еще раз чуть позже!"

    bot.reply_to(message, ai_response)

if __name__ == "__main__":
    bot.remove_webhook()
    # Берем ссылку на сервер напрямую или из настроек
    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://onrender.com")
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
