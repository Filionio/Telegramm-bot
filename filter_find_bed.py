import telebot
import config

bot = telebot.TeleBot(config.token)
filter_user = list()


def city_find(message):
    bot.send_message(message.chat.id, "Напишите город, в котором ищем ночлег")
    bot.register_next_step_handler(message, arrival_date)
@bot.message_handler(content_types=["text"])
def arrival_date(message):
    global filter_user
    filter_user.append(message.text)
    bot.send_message(message.chat.id, "Напишите дату заезда (например, 20.10.2023)")
    bot.register_next_step_handler(message, departure_date)
@bot.message_handler(content_types=["text"])
def departure_date(message):
    global filter_user
    filter_user.append(message.text)
    bot.send_message(message.chat.id, "Напишите дату выезда (например, 23.10.2023)")
    bot.register_next_step_handler(message, number_people)
@bot.message_handler(content_types=["text"])
def number_people(message):
    global filter_user
    filter_user.append(message.text)
    bot.send_message(message.chat.id, "Напишите количество человек (например, 2)")
    bot.register_next_step_handler(message, min_price)
@bot.message_handler(content_types=["text"])
def min_price(message):
    global filter_user
    filter_user.append(message.text)
    bot.send_message(message.chat.id, "Напишите минимальную цену (если не важно, то введите '0')")
    bot.register_next_step_handler(message, max_price)
@bot.message_handler(content_types=["text"])
def max_price(message):
    global filter_user
    filter_user.append(message.text)
    bot.send_message(message.chat.id, "Напишите максимальную цену")
    bot.register_next_step_handler(message, offers_screen)
@bot.message_handler(content_types=["text"])
def offers_screen(message):
    global filter_user
    filter_user.append(message.text)
    bot.send_message(message.chat.id, "Напишите сколько предложений ночлегов вам вывести на экран?")
    filter_user.append(message.text)

