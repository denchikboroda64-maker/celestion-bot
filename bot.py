import telebot
import requests

TG_TOKEN = "8761851210:AAGL39MaJj68VAMo4wv0SWxUcvsLtQXQK3M"
DEEPSEEK_API_KEY = "sk-2b01b0b2ae2f4874894b11d6da73be56"

bot = telebot.TeleBot(TG_TOKEN)
SYSTEM_PROMPT = "Ты — ассистент Целестион. Отвечай кратко, чётко, на русском языке."

print("🤖 Бот запущен!"@botbmessageage_handler(func=lambmessageage: True)
def handle_message(message):
    try:
     url = "https://siliconflow.cn"
        headers = {
            "Authorization": f"Bearer {DEEPSEAP_API_KEY}",
            "Content-Type"applicationion/json"
        }
        data = {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            "max_tokens": 1000
        }
        response = requests.post(url, json=data, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code} - {response.text}")
            bot.reply_to(message, "⚠️ Ошибка на стороне нейросети.")
            return
        bot_response = response.json()['choices']['message']['content']
        bot.reply_to(message, bot_response)
    except Exception as e:
        print(f"Ошибка в коде: {e}")
        bot.reply_to(message, "⚠️ Ошибка связи с нейросетью. Попробуй еще раз.")

bot.infinity_polling()
