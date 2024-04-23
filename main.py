import sqlalchemy
import telebot
from config import token
from SQLA_recs import *




bot = telebot.TeleBot(token)

users = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, text='Добро пожаловать. Данный бот создан для того чтобы принимать от жильцов показания и '
                               'отправлять их в местное ЖКХ.\n/help - получить информацию')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, text='Схема работы - простейшая, для того чтобы воспользоваться ботом нужно авторизоваться.'
                               '\n/auth - авторизация\n\nВозможные действия становятся доступны после авторизации.'
                               '\n/menu - получить клавиатуру с возможными действиями'
                               '\n\n"Отправить показания" - пункт для отправки показаний'
                               '\n"Отправить обращение" - пункт для отправки обращений в ЖКХ'
                               '\n"Оплатить услуги" - пункт для оплаты услуг'
                               '\n"Контакты" - пункт для получения контактов ЖКХ')


@bot.message_handler(commands=['menu'])
def send_menu(message):
    chat_id = message.chat.id

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    meters_data = telebot.types.KeyboardButton(text="Отправить показания")
    treatment = telebot.types.KeyboardButton(text="Отправить обращение")
    payment = telebot.types.KeyboardButton(text="Оплатить услуги")
    contacts = telebot.types.KeyboardButton(text="Контакты")

    keyboard.add(meters_data)
    keyboard.add(treatment)
    keyboard.add(payment)
    keyboard.add(contacts)


    bot.send_message(chat_id, text='Вам отправлена клавиатура с возможными действиями.', reply_markup=keyboard)


@bot.message_handler(commands=['auth'])
def send_welcome(message):
    bot.reply_to(message, text='Для авторизации отправьте вашу фамилию следующим сообщением.')
    bot.register_next_step_handler(message, last_name)


def last_name(message):
    try:
        get_user_by_last_name(message.text)
        bot.send_message(message.chat.id, "Введите номер лицевого счета")

    except sqlalchemy.exc.NoResultFound:
        bot.send_message(message.chat.id, "Пользователя с данной фамилией не найдено")


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.chat.id not in users:
        bot.send_message(message.chat.id, "Авторизуйтесь для работы с ботом"
                                          "\n/auth - авторизация")
        return None

    if message.text == "Отправить показания":
        bot.send_message(message.chat.id, "Здесь будет отправка показаний")
    elif message.text == "Отправить обращение":
        bot.send_message(message.chat.id, "Здесь будет отправка сообщений")
    elif message.text == "Оплатить услуги":
        bot.send_message(message.chat.id, "Здесь будет оплата услуг")
    elif message.text == "Контакты":
        bot.send_message(message.chat.id, "Здесь будут отправлятся контакты ЖКХ")
    else:
        bot.send_message(message.chat.id, "Выберите одно из возможных действий на клавиатуре."
                                          "\n/menu - чтобы получить клавиатуру")

bot.infinity_polling()