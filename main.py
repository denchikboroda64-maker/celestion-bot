import os
import telebot
import requests

# 1. НАСТРОЙКА КЛЮЧЕЙ И ТОКЕНОВ
# Скрипт сначала проверяет настройки Render (Environment), а если их там нет — берет прописанные ниже.
OPENROUTER_API_KEY = os.getenv("AI_KEY") or "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"
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN") or "8761851210:AAGL39MaJj68VAMo4wv0SWxUcvsLtQXQK3M"

# Инициализируем Телеграм-бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# 2. ФУНКЦИЯ ДЛЯ ЗАПРОСА К OPENROUTER
def ask_openrouter(user_message):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-chat",  # Самая быстрая и дешевая модель на данный момент
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Ошибка OpenRouter API: Код {response.status_code}\n{response.text}"
    except Exception as e:
        return f"Не удалось связаться с нейросетью: {str(e)}"

# 3. ОБРАБОТКА КОМАНД И СООБЩЕНИЙ В ТЕЛЕГРАМЕ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой ИИ-помощник на базе DeepSeek. Напиши мне что-нибудь, и я отвечу.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Показываем статус, что бот печатает ответ
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Отправляем текст в OpenRouter
    ai_response = ask_openrouter(message.text)
    
    # Возвращаем ответ пользователю в Telegram
    bot.reply_to(message, ai_response)

# 4. ЗАПУСК БОТА
if __name__ == "__main__":
    print("Бот успешно запущен и слушает сообщения...")
    bot.infinity_polling()
