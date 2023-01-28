import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import config
import telebot
bot = telebot.TeleBot(config.token)
def get_address_from_coords(message,coords):
    PARAMS = {
        "apikey": "3c7415d8-50ca-4962-93c1-e687e88a3301",
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    try:
        req = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = req.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str

    except Exception as e:
        return bot.send_message(message.chat.id,"Не могу определить адрес по этой локации/координатам." \
               "\n\nОтправь мне локацию или координаты (долгота, широта):")


@bot.message_handler(content_types=["text"])
def first_sms(message):
    bot.send_message(message.chat.id,'Отправь мне локацию или координаты (долгота, широта):')

def text(update, context):
    coords = update.message.text
    address_str = get_address_from_coords(coords)
    update.message.reply_text(address_str)

def location(update, context):
    message = update.message
    current_position = (message.location.longitude, message.location.latitude)
    coords = f"{current_position[0]},{current_position[1]}"
    address_str = get_address_from_coords(coords)
    update.message.reply_text(address_str)

def start_coord(message):
    dispatcher.add_handler(CommandHandler("mess", first_sms(message)))
    dispatcher.add_handler(MessageHandler(filters.text, text))
    dispatcher.add_handler(MessageHandler(filters.location, location))
    updater.start_polling()
    updater.idle()
