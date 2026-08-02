import os
import requests
from flask import Flask, request
import telebot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

AI_URL = "https://openrouter.ai"
AI_KEY = os.environ.get('AI_KEY', 'Bearer sk-or-v1-free-key') 

@app.route('/', methods=['GET'])
def index():
    return "Нейросеть активна!", 200

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    # Защита: проверяем, что в запросе вообще есть данные
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        if json_string:  # Если строка не пустая
            update = telebot.types.Update.de_json(json_string)
            if update and update.update_id:  # Проверяем, что это корректный апдейт от Telegram
                bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я Celestion — ваш бесплатный ИИ-ассистент. Напишите мне любой вопрос, и я отвечу!")

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
        ai_response = res_json['choices'][0]['message']['content']
        
    except Exception as e:
        ai_response = "Извините, нейросеть сейчас перегружена запросами. Попробуйте еще раз чуть позже!"

    bot.reply_to(message, ai_response)

if __name__ == "__main__":
    bot.remove_webhook()
    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
    if RENDER_URL:
        bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
