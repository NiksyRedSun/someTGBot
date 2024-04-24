import sqlalchemy
import telebot
from config import token
from SQLA_recs import *
from models import *




bot = telebot.TeleBot(token)

# нужен для авторизации
users = {}

#нужны для временного хранения данных, перед отправкой в бд
treatments = {}


# хэндлеры на старт, на помощь и на меню

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

# хэндлеры на авторизацию

@bot.message_handler(commands=['auth'])
def send_welcome(message):
    bot.reply_to(message, text='Для авторизации отправьте вашу фамилию следующим сообщением.')
    bot.register_next_step_handler(message, get_last_name)



def get_last_name(message):
    try:
        users[message.chat.id] = get_user_by_last_name(message.text)
        bot.send_message(message.chat.id, "Введите номер лицевого счета")
        bot.register_next_step_handler(message, get_id)

    except sqlalchemy.exc.NoResultFound:
        bot.send_message(message.chat.id, "Пользователя с данной фамилией не найдено"
                                            "\nПройдите авторизацию заново."
                                            "\n/auth - авторизация")

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


def get_id(message):
    try:
        if users[message.chat.id].id == int(message.text):
            bot.send_message(message.chat.id, "Вы успешно авторизованы.")
        else:
            del users[message.chat.id]
            bot.send_message(message.chat.id, "Данный лицевой счет не соответствует фамилии."
                                              "\nПройдите авторизацию заново."
                                              "\n/auth - авторизация")

    except ValueError:
        bot.send_message(message.chat.id, "При отправке лицевого счета используйте только числа. "
                                          "Повторите ввод лицевого счета заново.")
        bot.register_next_step_handler(message, get_id)

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


#хэндлеры на действия

@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.chat.id not in users:
        bot.send_message(message.chat.id, "Авторизуйтесь для работы с ботом"
                                          "\n/auth - авторизация")
        return None

    if message.text == "Отправить показания":
        bot.send_message(message.chat.id, "Введите значения первого и второго показателя по электричеству через пробел.")
        bot.register_next_step_handler(message, get_electricity)

    elif message.text == "Отправить обращение":
        bot.send_message(message.chat.id, "Следующим сообщением отправьте тему обращения.")
        bot.register_next_step_handler(message, treatment_theme)

    elif message.text == "Оплатить услуги":
        bot.send_message(message.chat.id, "Следующим сообщением отправьте сумму, которую хотите заплатить")
        bot.register_next_step_handler(message, payment)

    elif message.text == "Контакты":
        bot.send_message(message.chat.id, "Для личного обращения вы можете пройти по адресу "
                                          "ул. Пушкина, дом Колотушкина.")

    else:
        bot.send_message(message.chat.id, "Выберите одно из возможных действий на клавиатуре."
                                          "\n/menu - чтобы получить клавиатуру")


#получение данных по электричеству

def get_electricity(message):
    try:
        parameter1, parameter2 = tuple(map(lambda x: int(x), (message.text).split()))
        indicator = Indicator(client_id=users[message.chat.id].id, first_parameter=parameter1,
                              second_parameter=parameter2, source='Electricity', room_type="Common")
        save(indicator)
        bot.send_message(message.chat.id, "Данные успешно сохранены")
        bot.send_message(message.chat.id,
                         "Введите значения первого и второго показателя по воде на кухне через пробел.")
        bot.register_next_step_handler(message, get_kitchen)

    except ValueError:
        bot.send_message(message.chat.id, "При отправке показателей используйте только числа. "
                                          "Вводите только два показателя через пробел. "
                                          "Повторите ввод показателей по электричеству заново.")
        bot.register_next_step_handler(message, get_electricity)

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


#получение данных по воде на кухне

def get_kitchen(message):
    try:
        parameter1, parameter2 = tuple(map(lambda x: int(x), (message.text).split()))
        indicator = Indicator(client_id=users[message.chat.id].id, first_parameter=parameter1,
                              second_parameter=parameter2, source='Water', room_type="Kitchen")
        save(indicator)
        bot.send_message(message.chat.id, "Данные успешно сохранены")
        bot.send_message(message.chat.id,
                         "Введите значения первого и второго показателя по воде в ванной через пробел.")
        bot.register_next_step_handler(message, get_bath)

    except ValueError:
        bot.send_message(message.chat.id, "При отправке показателей используйте только числа. "
                                          "Вводите только два показателя через пробел. "
                                          "Повторите ввод показателей по воде на кухне заново.")
        bot.register_next_step_handler(message, get_kitchen)

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


#получение данных по воде в ванной

def get_bath(message):
    try:
        parameter1, parameter2 = tuple(map(lambda x: int(x), (message.text).split()))
        indicator = Indicator(client_id=users[message.chat.id].id, first_parameter=parameter1,
                              second_parameter=parameter2, source='Water', room_type="Bath")
        save(indicator)
        bot.send_message(message.chat.id, "Данные успешно сохранены. Вы отправили все показатели.")

    except ValueError:
        bot.send_message(message.chat.id, "При отправке показателей используйте только числа. "
                                          "Вводите только два показателя через пробел. "
                                          "Повторите ввод показателей по воде в ванной заново.")
        bot.register_next_step_handler(message, get_bath)

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


#хэндлеры по обращениям
def treatment_theme(message):
    try:
        treatments[message.chat.id] = Treatment(type=message.text, client_id=users[message.chat.id].id)
        bot.send_message(message.chat.id, "В следующем сообщение подробно опишите возникшую проблему.")
        bot.register_next_step_handler(message, treatment_text)

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


def treatment_text(message):
    try:
        treatments[message.chat.id].text = message.text
        bot.send_message(message.chat.id, "Спасибо за ваше обращение, мы ответим вам так скоро, как только сможем.")
        save(treatments[message.chat.id])
        del treatments[message.chat.id]

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


#оплата
def payment(message):
    try:
        int(message.text)
        bot.send_message(message.chat.id, "Спасибо за вашу оплату")

    except ValueError:
        bot.send_message(message.chat.id, "Повторите ввод оплаты, используя числовые значения")
        bot.register_next_step_handler(message, payment)

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


bot.infinity_polling()