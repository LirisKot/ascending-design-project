# simple_telegram_bot.py
"""
УПРОЩЕННЫЙ TELEGRAM БОТ БАЗЫ ДАННЫХ
===================================
Работает без .env файла - токен в коде
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)
from telegram.constants import ParseMode
from enum import Enum

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ВСТАВЬТЕ СЮДА ВАШ ТОКЕН БОТА
# Получите у @BotFather в Telegram
BOT_TOKEN = "8586680340:AAGajNmmTKkD95xCAt5kEwOrlUGKmqTfZVw"  # ← ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ТОКЕН


class BotState(Enum):
    """Состояния бота."""
    START = "start"
    MAIN_MENU = "main_menu"
    ARRAY_MENU = "array_menu"
    MATRIX_MENU = "matrix_menu"
    HELP = "help"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start."""
    keyboard = [
        [InlineKeyboardButton("📊 Массивы", callback_data="arrays")],
        [InlineKeyboardButton("🧮 Матрицы", callback_data="matrices")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """
🤖 *Бот для решения Задания 2*

Выберите категорию:
• 📊 Массивы - операции с массивами
• 🧮 Матрицы - операции с матрицами
• ❓ Помощь - инструкция по использованию
    """

    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help."""
    help_text = """
❓ *Помощь*

*Команды:*
/start - Начать работу
/help - Эта справка
/menu - Главное меню

*Операции с массивами:*
1. Создание массива
2. Суммирование массивов
3. Поиск общих элементов

*Операции с матрицами:*
1. Создание матрицы
2. Поворот матрицы
3. Транспонирование

*Примеры ввода:*
• Массив: `1, 2, 3, 4, 5`
• Матрица: `1, 2, 3\\n4, 5, 6\\n7, 8, 9`
    """

    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        help_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu."""
    keyboard = [
        [InlineKeyboardButton("📊 Массивы", callback_data="arrays")],
        [InlineKeyboardButton("🧮 Матрицы", callback_data="matrices")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "🏠 *Главное меню*"

    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий кнопок."""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "arrays":
        keyboard = [
            [InlineKeyboardButton("➕ Создать массив", callback_data="create_array")],
            [InlineKeyboardButton("🔢 Суммировать", callback_data="sum_arrays")],
            [InlineKeyboardButton("🔍 Общие элементы", callback_data="common_elements")],
            [InlineKeyboardButton("🔙 Назад", callback_data="menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = "📊 *Операции с массивами*"

        await query.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "matrices":
        keyboard = [
            [InlineKeyboardButton("➕ Создать матрицу", callback_data="create_matrix")],
            [InlineKeyboardButton("🔄 Повернуть", callback_data="rotate_matrix")],
            [InlineKeyboardButton("📐 Транспонировать", callback_data="transpose_matrix")],
            [InlineKeyboardButton("🔙 Назад", callback_data="menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = "🧮 *Операции с матрицами*"

        await query.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "help":
        help_text = """
❓ *Помощь*

Используйте кнопки для навигации.
Для операций ввода используйте текстовые сообщения.
        """

        keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(
            help_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "menu":
        keyboard = [
            [InlineKeyboardButton("📊 Массивы", callback_data="arrays")],
            [InlineKeyboardButton("🧮 Матрицы", callback_data="matrices")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = "🏠 *Главное меню*"

        await query.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "create_array":
        text = """
➕ *Создание массива*

Введите размер массива (число):
        """

        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="arrays")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

        # Сохраняем состояние
        context.user_data['awaiting_input'] = 'array_size'

    elif data == "sum_arrays":
        text = """
🔢 *Суммирование массивов*

Введите первый массив (числа через запятую):
Пример: `1, 2, 3`
        """

        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="arrays")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

        context.user_data['awaiting_input'] = 'array1'

    elif data == "create_matrix":
        text = """
➕ *Создание матрицы*

Введите количество строк:
        """

        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="matrices")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

        context.user_data['awaiting_input'] = 'matrix_rows'

    elif data == "rotate_matrix":
        text = """
🔄 *Поворот матрицы*

Введите квадратную матрицу (например 3x3)
        """

        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="matrices")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

        context.user_data['awaiting_input'] = 'rotate_matrix'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений."""
    user_input = update.message.text
    state = context.user_data.get('awaiting_input')

    if state == 'array_size':
        try:
            size = int(user_input)
            import random
            array = [random.randint(1, 100) for _ in range(size)]

            text = f"""
✅ *Массив создан*

Размер: {size}
Массив: `{array}`
            """

            keyboard = [[InlineKeyboardButton("📊 Еще массив", callback_data="create_array")],
                        [InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

            context.user_data.pop('awaiting_input', None)

        except ValueError:
            await update.message.reply_text(
                "❌ Пожалуйста, введите целое число!"
            )

    elif state == 'array1':
        try:
            array1 = [int(x.strip()) for x in user_input.split(',')]
            context.user_data['array1'] = array1
            context.user_data['awaiting_input'] = 'array2'

            text = f"""
📥 Первый массив: `{array1}`

Теперь введите второй массив (такой же длины):
            """

            await update.message.reply_text(
                text,
                parse_mode=ParseMode.MARKDOWN
            )

        except ValueError:
            await update.message.reply_text(
                "❌ Ошибка! Введите числа через запятую.\nПример: `1, 2, 3`"
            )

    elif state == 'array2':
        try:
            array2 = [int(x.strip()) for x in user_input.split(',')]
            array1 = context.user_data.get('array1', [])

            if len(array1) != len(array2):
                await update.message.reply_text(
                    f"❌ Массивы разной длины! Первый: {len(array1)}, второй: {len(array2)}"
                )
                return

            result = [a + b for a, b in zip(array1, array2)]

            text = f"""
✅ *Массивы суммированы*

Массив 1: `{array1}`
Массив 2: `{array2}`
Результат: `{result}`
            """

            keyboard = [[InlineKeyboardButton("🔢 Еще суммирование", callback_data="sum_arrays")],
                        [InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

            context.user_data.pop('awaiting_input', None)
            context.user_data.pop('array1', None)

        except ValueError:
            await update.message.reply_text(
                "❌ Ошибка! Введите числа через запятую."
            )

    elif state == 'matrix_rows':
        try:
            rows = int(user_input)
            if rows <= 0:
                raise ValueError

            context.user_data['matrix_rows'] = rows
            context.user_data['awaiting_input'] = 'matrix_cols'

            text = f"📥 Строк: {rows}\n\nТеперь введите количество столбцов:"

            await update.message.reply_text(text)

        except ValueError:
            await update.message.reply_text("❌ Введите положительное целое число!")

    elif state == 'matrix_cols':
        try:
            cols = int(user_input)
            rows = context.user_data.get('matrix_rows', 0)

            if cols <= 0:
                raise ValueError

            import random
            matrix = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]

            matrix_text = "\n".join([f"`{row}`" for row in matrix])

            text = f"""
✅ *Матрица создана*

Размер: {rows}×{cols}

Матрица:
{matrix_text}
            """

            keyboard = [[InlineKeyboardButton("➕ Еще матрицу", callback_data="create_matrix")],
                        [InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

            context.user_data.pop('awaiting_input', None)
            context.user_data.pop('matrix_rows', None)

        except ValueError:
            await update.message.reply_text("❌ Введите положительное целое число!")

    elif state == 'rotate_matrix':
        try:
            lines = user_input.strip().split('\n')
            matrix = []

            for line in lines:
                row = [int(x.strip()) for x in line.split(',')]
                matrix.append(row)

            # Проверяем квадратность
            n = len(matrix)
            for row in matrix:
                if len(row) != n:
                    raise ValueError("Матрица должна быть квадратной")

            # Поворачиваем
            rotated = [[matrix[n - 1 - j][i] for j in range(n)] for i in range(n)]

            original_text = "\n".join([f"`{row}`" for row in matrix])
            rotated_text = "\n".join([f"`{row}`" for row in rotated])

            text = f"""
✅ *Матрица повернута*

*Исходная ({n}×{n}):*
{original_text}

*Повернутая:*
{rotated_text}
            """

            keyboard = [[InlineKeyboardButton("🔄 Еще повернуть", callback_data="rotate_matrix")],
                        [InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

            context.user_data.pop('awaiting_input', None)

        except Exception as e:
            await update.message.reply_text(
                f"❌ Ошибка: {str(e)}\nПроверьте формат ввода."
            )

    else:
        # Если не ожидаем ввода, показываем меню
        keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Используйте /start для начала работы",
            reply_markup=reply_markup
        )


def main():
    """Запуск бота."""
    print("=" * 60)
    print("🤖 ЗАПУСК УПРОЩЕННОГО TELEGRAM БОТА")
    print("=" * 60)

    # Проверка токена
    if BOT_TOKEN == "ВАШ_ТОКЕН_ЗДЕСЬ":
        print("❌ ОШИБКА: Вы не установили токен бота!")
        print("\nКак получить токен:")
        print("1. Откройте Telegram")
        print("2. Найдите @BotFather")
        print("3. Отправьте /newbot")
        print("4. Следуйте инструкциям")
        print("5. Скопируйте токен (выглядит как: 1234567890:ABCdefGHIjkl...")
        print("\nЗамените 'ВАШ_ТОКЕН_ЗДЕСЬ' в коде на реальный токен")
        return

    print(f"✅ Токен: {BOT_TOKEN[:15]}...")
    print("📱 Бот запускается...")
    print("🔗 Перейдите в Telegram и найдите своего бота")
    print("=" * 60)

    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()