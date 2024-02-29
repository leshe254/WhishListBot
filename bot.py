import telebot
import time
from tokenbot import token
from gsheets import add_new_whish, get_whishlist
from requests.exceptions import RequestException

# Задаем токен для телебота и игнорируем висячие сообщения
bot = telebot.TeleBot(token, skip_pending=True)

# Кнопочки для меню
btns = ["Добавить хотелку", "Посмотреть свои хотелки", "Посмотреть чужие хотелки", "Вернуться назад"]

# ID чатов для пересылки сообщений о новых обращениях
chatids = [
    ["Алексей", "@lesssd", 362796634],
    ["Полина", "@polinka21471", 719454990],
]


@bot.message_handler(content_types=['text'])
def start_message(message):
    print(message.chat.id)
    user_nik = "@" + str(message.from_user.username)
    # Приветствие собеседника!
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}!")
    bot.send_message(message.chat.id, 'Выбери действие', reply_markup=btnmarkup)
    bot.register_next_step_handler(message, second_message, user_nik)


def second_message(message, user_nik):
    activity = str(message.text)
    if(activity == "None"):
        bot.send_message(message.chat.id, 'Мы распознаём только текстовые сообщения', reply_markup=btnmarkup)
        bot.register_next_step_handler(message, second_message, user_nik)
    elif(activity in btns):
        if(activity == "Добавить хотелку"):
            bot.send_message(message.chat.id, 'Напиши, что хочешь', reply_markup=backmarkup)
            bot.register_next_step_handler(message, add_new, user_nik)
        elif(activity == "Посмотреть свои хотелки"):
            # Чтение гугл таблицы, поиск строк, где определённое поле = никнейму, вывод в сообщение
            whishs = get_whishlist(user_nik, 1)
            if(len(whishs) != 0):
                bot.send_message(message.chat.id, 'Список:')
                for i in whishs:
                    bot.send_message(message.chat.id, i)
            else:
                bot.send_message(message.chat.id, 'Список пуст :(')
            bot.send_message(message.chat.id, 'Что будем делать дальше?', reply_markup=btnmarkup)
            bot.register_next_step_handler(message, second_message, user_nik)
        elif(activity == "Посмотреть чужие хотелки"):
            # Чтение гугл таблицы, поиск строк, где определённое поле = никнейму, вывод в сообщение
            whishs = get_whishlist(user_nik, 2)
            if(len(whishs) != 0):
                bot.send_message(message.chat.id, 'Список:')
                for i in whishs:
                    bot.send_message(message.chat.id, i)
            else:
                bot.send_message(message.chat.id, 'Список пуст :(')
            bot.send_message(message.chat.id, 'Что будем делать дальше?', reply_markup=btnmarkup)
            bot.register_next_step_handler(message, second_message, user_nik)
        elif(activity == "Вернуться назад"):
            bot.send_message(message.chat.id, f"Не забывай про нас, {message.chat.first_name}!\nПиши, когда вздумается...", reply_markup=btnmarkup)
            bot.register_next_step_handler(message, start_message)
        else:
            bot.send_message(message.chat.id, 'Выбери что-то из списка!', reply_markup=btnmarkup)
            bot.register_next_step_handler(message, second_message, user_nik)


def add_new(message, user_nik):
    whish = str(message.text)
    # Проверка на медиа-контент или комманду
    if(whish != "None" and whish[0] != '/'):
        if(whish == "Вернуться назад"):
            # Возврат к основному меню
            bot.send_message(message.chat.id, 'Выбери, что хочешь сделать!', reply_markup=btnmarkup)
            bot.register_next_step_handler(message, second_message, user_nik)
        else:
            # Запись новой хотелки
            bot.send_message(message.chat.id, 'Мы записали твое желание, пиши, когда придумаешь что-то ещё!', reply_markup=startmarkup)
            bot.register_next_step_handler(message, start_message)
            # Функция для работы с таблицами
            add_new_whish(user_nik, whish)
            # Оповещение о новой хотелке
            if(user_nik == chatids[0][1]):
                bot.send_message(chatids[1][2], f'{chatids[0][1]} что-то придумал!')
            else:
                bot.send_message(chatids[0][2], f'{chatids[1][1]} что-то придумал!')
    else:
        bot.send_message(message.chat.id, 'Мы распознаём только текстовые сообщения', reply_markup=backmarkup)
        bot.register_next_step_handler(message, add_new, user_nik)

if __name__ == '__main__':
    # Создаем клаву для "/start"
    startmarkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    startbtn = telebot.types.KeyboardButton("/start")
    startmarkup.add(startbtn)
    # Создаем клавиатуру для действий
    btnmarkup = telebot.telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for btn in btns:
        itemtmp = telebot.telebot.types.KeyboardButton(btn)
        btnmarkup.add(itemtmp)
    # Создаем ккнопку назад
    backmarkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    backbtn = telebot.types.KeyboardButton("Вернуться назад")
    backmarkup.add(backbtn)

    # Запуск бота
    while True:
        try:
            bot.infinity_polling(timeout=90, long_polling_timeout=5)
        except RequestException as err:
            print(err)
            print('Разрыв коннекта до телеграмма...')
            time.sleep(15)
            print('Переподключение...')
