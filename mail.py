
import telebot
import config
from telebot import types
import time

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def welcom(message):
    """Функция приветствия
    Добавляет начальное изображение с приветственным текстом
    Добавляет 4 кнопки для пользователя"""
    sti = open("static/welcom.webp","rb")
    bot.send_sticker(message.chat.id,sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("⛺Искать ночлег по фильтру🏕")
    item2 = types.KeyboardButton("🗺Искать ночлег ближайший🗺")
    item3 = types.KeyboardButton("🤓История запросов🤓")
    item4 = types.KeyboardButton("❓Помощь❓")
    markup.add(item1,item2,item3,item4)

    bot.send_message(message.chat.id,"Добро пожаловать, "
                                     "\nЯ помощник по поиску ночлега... "
                                     "\nВы ищете где переночевать в другом городе?"
                                     "\nУ меня есть 4 кнопки: "
                                     "\n1- '⛺Искать ночлег по фильтру🏕'"
                                     "\n2- '🗺Искать ночлег ближайший🗺'"
                                     "\n3- '🤓История запросов🤓'"
                                     "\n4- '❓Помощь❓'",
                     parse_mode="html", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def choose_items(message):
    """Функция кнопок
    После старта пользователь выбирает одну из доступных кнопок и выводит нужное на экран"""
    if message.chat.type == "private":
        if message.text == "⛺Искать ночлег по фильтру🏕":
            filter_user = list()

            def city_find(message):
                """Если пользователь выбрал 1 кнопку, то запрашиваются данные для фильтра и поиску по сайту AirBnb.ru"""
                bot.send_message(message.chat.id, "Напишите город, в котором ищем ночлег")
                bot.register_next_step_handler(message, arrival_date)


            def arrival_date(message):
                nonlocal filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id, "Напишите дату заезда"
                                                  "\n(год, месяц, день, например, 2023-09-10)")
                bot.register_next_step_handler(message, departure_date)

            def departure_date(message):
                nonlocal filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id, "Напишите дату выезда"
                                                  "\n(год, месяц, день, например, 2023-09-13)")
                bot.register_next_step_handler(message, number_people)

            def number_people(message):
                nonlocal filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id, "Напишите количество человек (например, 2)")
                bot.register_next_step_handler(message, offers_screen)

            def offers_screen(message):
                nonlocal filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id, "Напишите сколько предложений ночлегов вам вывести на экран?"
                                                  "\n от 1 до 8")
                bot.register_next_step_handler(message,output_result)

            def output_result(message):
                nonlocal filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id,'Для вывода результата напишите что-нибудь')
                bot.register_next_step_handler(message,API_find)

            def API_find(message):
                """Функция поиска
                Заданные параметры отправляются для поиска отеля и возвращают ссылки на отели, а также их 2 фотографии
                *также ведется подсчет работы функции*"""
                nonlocal filter_user
                import find_bed_API
                result_site,result_image = find_bed_API.find_rapid(filter_user)
                tic = time.perf_counter()
                for index,page in enumerate(result_site):
                    for image in result_image[index]:
                        bot.send_message(message.chat.id,image)
                    bot.send_message(message.chat.id,page)
                    bot.send_message(message.chat.id,f'Вариант номер: {index+1}\n')
                toc = time.perf_counter()
                bot.send_message(message.chat.id,f"Вычисление заняло {toc - tic:0.4f} секунд")



            filter_user = list()
            city_find(message)


        elif message.text == "🗺Искать ночлег ближайший🗺":
            bot.send_message(message.chat.id, "Успешно")

        elif message.text == "🤓История запросов🤓":
            bot.send_message(message.chat.id, "Успешно")

        elif message.text == "❓Помощь❓":
            bot.send_message(message.chat.id, "Сведения о командах\n"
                                              "Помощь - помощь по командам\n"
                                              "Искать ночлег по фильтру- по заданным вами параметрами будет произведен поиск\n"
                                              "Искать ночлег ближайший — по отправленной вами геолокации будет произведен поиск отелей\n"
                                              "История запросов — вывод истории поиска отелей")



bot.polling(none_stop= True)
