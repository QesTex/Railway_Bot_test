import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! 👋\n"
        f"Я простой тестовый бот.\n"
        f"Отправь мне любое сообщение, и я его повторю."
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 Доступные команды:
/start - Начать работу с ботом
/help - Получить справку
/echo <текст> - Эхо-ответ

Просто отправь мне сообщение, и я его повторю!
    """
    await update.message.reply_text(help_text)

# Команда /echo
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        text = ' '.join(context.args)
        await update.message.reply_text(f"📢 Эхо: {text}")
    else:
        await update.message.reply_text("Напиши текст после команды /echo")

# Обработка текстовых сообщений
async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Вы сказали: {text}")

# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка: {context.error}")

def main():
    # Получение токена из переменной окружения
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Ошибка: TELEGRAM_BOT_TOKEN не установлен!")
        return

    # Создание приложения
    application = Application.builder().token(token).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)

    # Запуск бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_UPDATES)

if __name__ == '__main__':
    main()
