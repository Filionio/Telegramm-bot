
import telebot
import config
from telebot import types
import time
import sqlite3
import tracemalloc
import asyncio
from aiogram.dispatcher.filters import Command

from sql import add,hist

tracemalloc.start()
filter_user = list()
filter_us = []
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
    global bot
    """Функция кнопок
    После старта пользователь выбирает одну из доступных кнопок и выводит нужное на экран"""
    if message.chat.type == "private":
        if message.text == "⛺Искать ночлег по фильтру🏕":


            def city_find(message):
                """Если пользователь выбрал 1 кнопку, то запрашиваются данные для фильтра и поиску по сайту AirBnb.ru"""
                bot.send_message(message.chat.id, "Напишите город, в котором ищем ночлег")
                bot.register_next_step_handler(message, arrival_date)


            def arrival_date(message):
                global filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id, "Напишите дату заезда"
                                                  "\n(год, месяц, день, например, 2023-09-10)")
                bot.register_next_step_handler(message, departure_date)

            def departure_date(message):
                global filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id, "Напишите дату выезда"
                                                  "\n(год, месяц, день, например, 2023-09-13)")
                bot.register_next_step_handler(message, number_people)

            def number_people(message):
                global filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id, "Напишите количество человек (например, 2)")
                bot.register_next_step_handler(message, offers_screen)

            def offers_screen(message):
                global filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id, "Напишите сколько предложений ночлегов вам вывести на экран?"
                                                  "\n от 1 до 8")
                bot.register_next_step_handler(message,output_result)

            def output_result(message):
                global filter_user
                filter_user.append(message.text)
                bot.send_message(message.chat.id,'Для вывода результата напишите что-нибудь')
                bot.register_next_step_handler(message,API_find)

            def API_find(message):
                """Функция поиска
                Заданные параметры отправляются для поиска отеля и возвращают ссылки на отели, а также их 2 фотографии
                *также ведется подсчет работы функции*"""
                global filter_user
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
                bot.register_next_step_handler(message,asyncio.run(add_cmd(message)))

            async def add_cmd(message):
                s = filter_user
                await add(s)
                bot.send_message(message.chat.id,'История успешно добавлена!!!')
            global filter_user
            city_find(message)


        elif message.text == "🗺Искать ночлег ближайший🗺":

            @bot.message_handler(commands=["geo"])
            def geo(message):
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
                keyboard.add(button_geo)
                bot.send_message(message.chat.id,"🤓Нажми на кнопку и передай мне свое местоположение🤓"
                                                 "\n🗺Либо отправь мне точку на карте вручную🗺",reply_markup=keyboard)
                bot.register_next_step_handler(message,location)

            @bot.message_handler(content_types=["location"])
            def location(message):
                import find_bed_geo
                if message.location is not None:
                    global filter_us
                    bot.send_message(message.chat.id,f"Ваша широта: {round(message.location.latitude,2)}; Ваша долгота: {round(message.location.longitude,2)}")
                    latitude = round(message.location.latitude,2)
                    longitude = round(message.location.longitude, 2)
                    def start_filter(message):
                        bot.send_message(message.chat.id,'Сколько предложений вам вывести?(От 1 до 8)')
                        bot.register_next_step_handler(message,total_site)
                    def total_site(message):
                        global filter_us
                        filter_us.append(message.text)
                        bot.send_message(message.chat.id,'Когда планируете заехать?(Например,2023-09-10)')
                        bot.register_next_step_handler(message, arrival_f)

                    def arrival_f(message):
                        global filter_us
                        filter_us.append(message.text)
                        bot.send_message(message.chat.id,'Когда планируете выехать?(Например,2023-09-13)')
                        bot.register_next_step_handler(message, departure_f)

                    def departure_f(message):
                        global filter_us
                        filter_us.append(message.text)
                        bot.send_message(message.chat.id,"Для вывода напишите что-нибудь")
                        bot.register_next_step_handler(message, user_find)

                    def user_find(message):
                        global filter_us
                        result_site,result_image = find_bed_geo.find_geo(latitude,longitude,filter_us)
                        tic = time.perf_counter()
                        for index, page in enumerate(result_site):
                            for image in result_image[index]:
                                bot.send_message(message.chat.id, image)
                            bot.send_message(message.chat.id, page)
                            bot.send_message(message.chat.id, f'Вариант номер: {index + 1}\n')
                        toc = time.perf_counter()
                        bot.send_message(message.chat.id, f"Вычисление заняло {toc - tic:0.4f} секунд")
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton("⛺Искать ночлег по фильтру🏕")
                        item2 = types.KeyboardButton("🗺Искать ночлег ближайший🗺")
                        item3 = types.KeyboardButton("🤓История запросов🤓")
                        item4 = types.KeyboardButton("❓Помощь❓")
                        markup.add(item1, item2, item3, item4)
                        bot.send_message(message.chat.id,"!Продолжите поиск!"
                                                         "\n1- '⛺Искать ночлег по фильтру🏕'"
                                                          "\n2- '🗺Искать ночлег ближайший🗺'"
                                                          "\n3- '🤓История запросов🤓'"
                                                          "\n4- '❓Помощь❓'",
                                         parse_mode="html", reply_markup=markup)
                        choose_items(message)

                    start_filter(message)
                else:
                    bot.send_message(message.chat.id,'Неправильно введены данные')
                    bot.register_next_step_handler(message,welcom)

            geo(message)




        elif message.text == "🤓История запросов🤓":
            async def hist_cmd(message):
                info = await hist()
                bot.send_message(message.chat.id,"Город")
                bot.send_message(message.chat.id,info[0])

                bot.send_message(message.chat.id,"Дата заезда")
                bot.send_message(message.chat.id,info[1])

                bot.send_message(message.chat.id,"Дата выезда")
                bot.send_message(message.chat.id,info[2])

                bot.send_message(message.chat.id,"Дата кол-во гостей")
                bot.send_message(message.chat.id,info[3])

                bot.send_message(message.chat.id,"Кол-во постов")
                bot.send_message(message.chat.id,info[4])


            bot.send_message(message.chat.id, "Вывожу историю запросов")
            asyncio.run(hist_cmd(message))




        elif message.text == "❓Помощь❓":
            bot.send_message(message.chat.id, "Сведения о командах\n"
                                              "Помощь - помощь по командам\n"
                                              "Искать ночлег по фильтру- по заданным вами параметрами будет произведен поиск\n"
                                              "Искать ночлег ближайший — по отправленной вами геолокации будет произведен поиск отелей\n"
                                              "История запросов — вывод истории поиска отелей")



bot.polling(none_stop= True)
