# run_bot.py
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    print("❌ Ошибка: не найден BOT_TOKEN в .env файле")
    print("Создайте файл .env с содержимым:")
    print("BOT_TOKEN=ваш_токен_бота")
    print("\nПолучить токен можно у @BotFather в Telegram")
    exit(1)

# Запуск бота
from telegram_bot import main

if __name__ == "__main__":
    main()