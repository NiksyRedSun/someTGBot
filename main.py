import telebot
from config import token




bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, text='Добро пожаловать. Данный бот создан для того чтобы принимать от жильцов показания и '
                               'отправлять их в местное ЖКХ.\n/help - получить информацию')


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, text='Схема работы - простейшая, для того чтобы воспользоваться ботом нужно авторизоваться.'
                               '\n/auth - авторизация\n/menu - получить клавиатуру с возможными действиями')


bot.infinity_polling()