import sqlalchemy
import telebot
from config import token
from SQLA_recs import *
from models import *
from invoice.invoice_generator import make_pdf



bot = telebot.TeleBot(token)

# нужен для авторизации
users = {}


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
    meters_data_electricity = telebot.types.KeyboardButton(text="Отправить показания электричества")
    meters_data_water = telebot.types.KeyboardButton(text="Отправить показания воды")
    treatment = telebot.types.KeyboardButton(text="Отправить обращение")
    payment = telebot.types.KeyboardButton(text="Оплатить услуги")
    contacts = telebot.types.KeyboardButton(text="Контакты")

    keyboard.add(meters_data_electricity)
    keyboard.add(meters_data_water)
    keyboard.add(treatment)
    keyboard.add(payment)
    keyboard.add(contacts)


    bot.send_message(chat_id, text='Вам отправлена клавиатура с возможными действиями.', reply_markup=keyboard)

# хэндлеры на авторизацию

@bot.message_handler(commands=['auth'])
def send_welcome(message):
    bot.reply_to(message, text='Для авторизации отправьте ваши Фамилию Имя Отчество следующим сообщением'
                               ' последовательно, через пробел.')
    bot.register_next_step_handler(message, get_full_name)



def get_full_name(message):
    try:
        last_name, first_name, middle_name = (message.text).split()
        users[message.chat.id] = get_user(last_name, first_name, middle_name)
        bot.send_message(message.chat.id, "Введите номер лицевого счета")
        bot.register_next_step_handler(message, get_id)

    except sqlalchemy.exc.NoResultFound:
        bot.send_message(message.chat.id, "Пользователя с данными ФИО не найдено"
                                            "\nПройдите авторизацию заново."
                                            "\n/auth - авторизация")
    except ValueError:
        bot.send_message(message.chat.id, "Вводите только ФИО (3 слова последовательно), через пробел"
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

    elif message.text == "Отправить показания электричества":
        bot.send_message(message.chat.id, "Последовательно, через пробел,"
                                          " введите показания счетчиков электричества за день и ночь.")
        bot.register_next_step_handler(message, get_electricity)

    elif message.text == "Отправить показания воды":
        bot.send_message(message.chat.id,
                         "Последовательно, через пробел, введите показания счетчиков горячей и холодной воды на кухне.")
        bot.register_next_step_handler(message, get_kitchen)

    elif message.text == "Отправить обращение":
        bot.send_message(message.chat.id, "Следующим сообщением введите тему обращения."
                                          " Затем перейдите на следующую строку и подробно распишите причину обращения.")
        bot.register_next_step_handler(message, make_treatment)

    elif message.text == "Оплатить услуги":
        bot.send_message(message.chat.id, "Следующим сообщением отправьте сумму, "
                                          "которую хотите заплатить за комунальные услуги.")
        bot.register_next_step_handler(message, payment)

    elif message.text == "Контакты":
        bot.send_message(message.chat.id, "Для личного обращения вы можете пройти по адресу "
                                          "г. Уфа, ул. Комсомольская 165/1, МКУ УЖХ г. Уфы, "
                                          "контактный телефон: 8(347)233-66-33.")

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


    except ValueError:
        bot.send_message(message.chat.id, "При отправке показаний используйте только числа. "
                                          "Вводите только два показания: за день и ночь через пробел. "
                                          "Повторите ввод показаний счетчиков электричества заново.")
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
                         "Последовательно, через пробел, введите показания счетчиков горячей и холодной воды в ванной.")
        bot.register_next_step_handler(message, get_bath)

    except ValueError:
        bot.send_message(message.chat.id, "При отправке показаний используйте только числа. "
                                          "Вводите только два показания: по горячей и по холодной воде через пробел. "
                                          "Повторите ввод показаний счетчиков горячей и холодной воды в кухне заново.")
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
        bot.send_message(message.chat.id, "Данные успешно сохранены.")

    except ValueError:
        bot.send_message(message.chat.id, "При отправке показаний используйте только числа. "
                                          "Вводите только два показания: по горячей и по холодной воде через пробел. "
                                          "Повторите ввод показаний счетчиков горячей и холодной воды в ванной заново.")
        bot.register_next_step_handler(message, get_bath)

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")



#хэндлеры по обращениям
def make_treatment(message):
    try:
        theme, text = message.text.split('\n', 1)
        treatment = Treatment(client_id=users[message.chat.id].id, type=theme, text=text)
        save(treatment)
        bot.send_message(message.chat.id, "Спасибо за ваше обращение, мы ответим вам так скоро, как только сможем.")

    except ValueError:
        bot.send_message(message.chat.id, "Не произошел перенос строки после темы обращения."
                                          "Повторите ввод, введите тему обращения, затем с помощью ENTER перейдите"
                                          " на другую строку и подробно распишите причину обращения")
        bot.register_next_step_handler(message, make_treatment)

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


#оплата
def payment(message):
    # try:
        int(message.text)
        bot.send_message(message.chat.id, "Спасибо за вашу оплату, квитанция будет отправлена следующим сообщением")
        make_pdf(users[message.chat.id].last_name + " " + users[message.chat.id].first_name + " " +  users[message.chat.id].middle_name,
                 users[message.chat.id].id, users[message.chat.id].address, message.text)
        f = open(r"invoice\demo.pdf", "rb")
        bot.send_document(message.chat.id, f)

    # except ValueError:
    #     bot.send_message(message.chat.id, "Повторите ввод оплаты, используя числовые значения")
    #     bot.register_next_step_handler(message, payment)
    #
    # except:
    #     bot.send_message(message.chat.id, "Что-то пошло не так, обратитесь к администратору для разъяснений.")


bot.infinity_polling()