#Это упрощённая версия бота, aka "Вставил и пошёл", для таких лентяев как я 😝

import telegram
import openai

# API ключи
telegram_api_key = "YOUR_TELEGRAM_API_KEY"
openai_api_key = "YOUR_OPENAI_API_KEY"

# Создание бота
bot = telegram.Bot(token=telegram_api_key)

# Инициализация OpenAI API
openai.api_key = openai_api_key

# Обработчик сообщений
def handle_message(update, context):
    # Получаем текст сообщения
    message_text = update.message.text

    # Получаем ответ от OpenAI
    response = openai.Completion.create(
        engine="davinci",
        prompt=message_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Отправляем ответ пользователю
    bot.send_message(chat_id=update.message.chat_id, text=response.choices[0].text)

# Создаем и запускаем бота
updater = telegram.ext.Updater(token=telegram_api_key, use_context=True)
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()
