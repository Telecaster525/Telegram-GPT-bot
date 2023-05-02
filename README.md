# Telegram GPT bot

# Краткий туториал: "Как написать своего умного телеграм-ботика, который подскажет вам, как приготовить пасту альфредо 😊 ?"

<b>Писать будем на Питоне, так проще и быстрее.</b>

Для начала нужно просто создать каталог:

```
mkdir chatgptbot
cd chatgptbot
```

Затем следует настроить виртуальную среду Python и активировать её:

```
python3 -m venv env=
source env/bin/activate
```

В папке chatbot создадим два файла:

1. bot.py

2. copilot.py

Сперва разберёмся с файлом copilot.py.

Установим openai и другие библиотеки:

```
pip install openai
pip install python-dotenv
```

Импортируем библиотеки:

```
import os
import json
from dotenv import load_dotenv
import openai
```

# Функции

Создадим класс Copilot и добавим две функции:

1. clear_text - будет отвечать за очистку лишних пробелов.

2. get_answer - будте отвечать за получение ответа. Вызывает класс *Completion* из библиотеки *openai*. Чтобы продолжить наш запрос, потребуется API-key.

```
class Copilot:

    def clear_text(self, text):
        a = text.replace("\n", " ")
        b = a.split()
        c = " ".join(b)

        return c

    def get_answer(self, question):
        prompt = question
        
        load_dotenv()

        openai.api_key = os.getenv("CHAT_GPT3_API_KEY")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=512,
            temperature=0.5,
        )

        json_object = response

        # Convert the JSON object to a JSON string
        json_string = json.dumps(json_object)

        # Parse the JSON string using json.loads()
        parsed_json = json.loads(json_string)

        text = parsed_json['choices'][0]['text']
        cleared_text = self.clear_text(text)
        
        return cleared_text
```

# Получение API-key GPT

Следует преейти на сайт *openai* и войти/зарегистрироваться. После успешного входа в учётную запись перейдите в раздел "API keys" и сгенерируйте новый API-key.

Создадим .env файл:

```
touch .env
```

Добавим API-key:

```
CHAT_GPT3_API_KEY = paste here your API-key
```

Ниже представлено его использование:

```
copilot = Copilot()
a = copilot.get_answer("Hello, there!")
print(a)
```

# А вот и сам Телеграм-бот

Установим и импортируем библиотеки:

```
pip install python-telegram-bot --pre
pip install requests
```

```
import os
import json
import requests
import time

from copilot import Copilot
from dotenv import load_dotenv

from telegram import (
    ReplyKeyboardMarkup,
    Update,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    )
```

Перейдём к файлу .env:

Добавим токен Телеграм-бота (который был ранее получем в BotFather):

```
TELEGRAM_BOT_TOKEN = paste your Telegram BOT-token
```

Используем *conv_handler* и сделаем Телеграм-бота масштабируемым для будущих обновленйи:

```
if __name__ == '__main__':
    load_dotenv()

    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).read_timeout(100).get_updates_read_timeout(100).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTRY_STATE: [
                MessageHandler(filters.Regex('^Back$'), start),
                MessageHandler(filters.Regex('^Question-Answering$'), pre_query_handler),
            ],
            QUESTION_STATE: [
                MessageHandler(filters.Regex('^Back$'), start),
                MessageHandler(filters.TEXT, pre_query_answer_handler),
            ],
        },
        fallbacks=[],
    )
    
    application.add_handler(conv_handler)

    print("Bot is running ...")
    application.run_polling()
```

Создадим функцию, которую можно будет повторно использовать:

```
def _generate_copilot(prompt: str):
    """Gets answer from copilot"""
    
    copilot = Copilot()
    c = copilot.get_answer(prompt)

    return c
```

Добавим команду */start*:

```
async def start(update: Update, context: ContextTypes):
    """Start the conversation and ask user for an option."""

    button = [[KeyboardButton(text="Question-Answering")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Choose an option: 👇🏻",
        reply_markup=reply_markup,
    )

    return ENTRY_STATE
```

Создадим функцию для пользовательского ввода:

```
#Handling the question
async def pre_query_handler(update: Update, context: ContextTypes):
    """Ask the user for a query."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Enter your text: 👇🏻",
        reply_markup=reply_markup,
    )

    return QUESTION_STATE
```

Обработка пользовательского ввода (*text*) и генерация текста (*answer*):

```
#Handling the answer
async def pre_query_answer_handler(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )

    question = update.message.text

    answer = _generate_copilot(question)
    context.user_data['answer'] = answer

    await update.message.reply_text(
        answer, 
        reply_markup=reply_markup,
    )

    return QUESTION_STATE
```

Ура! Теперь вы можете выбрать любой из предложенных свежеиспеченным ботом рецептов!

Подводные камни: API-key требует токены, а они в свою очередь стоять дЕнЯг 😁
