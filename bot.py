import telebot
import atexit
from telebot import types
import uuid
import logging
from model import llm_chain

# Замените 'YOUR_BOT_API_TOKEN' на ваш токен API бота
bot = telebot.TeleBot('7198636310:AAHuSgOuDLPa9WgfOvYTDRiPLqVZmZJydRE')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('log_file_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info('Started')

# Приветственное сообщение
welcome_message = (
    "Привет!!!"
)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, welcome_message)

@bot.message_handler(content_types=['text'])
def send_answer(message):
    chat_id = message.chat.id
    question = message.text #это то что спросили
    print(question)


    answer = llm_chain(question) #это то что вернет модель
    bot.send_message(chat_id, answer)
def notify_start():
    print('BOT STARTED')
    bot.send_message(5293492345, "✅ Бот запущен")


def notify_stop():
    print('BOT STOPPED')
    bot.send_message(5293492345, "⛔️ Бот выключен или перезапускается")


atexit.register(notify_stop)


def run_bot():
    notify_start()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)


run_bot()
