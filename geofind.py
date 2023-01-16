import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import config

def get_address_from_coords(coords):
    PARAMS = {
        "apikey": "ТОКЕН_ГЕОКОДЕРА",
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str

    except Exception as e:
        return "Не могу определить адрес по этой локации/координатам." \
               "\n\nОтправь мне локацию или координаты (долгота, широта):"



def start(update, context):
    update.message.reply_text('Отправь мне локацию или координаты (долгота, широта):')

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

def main():
    updater = Updater(config.token)
    dispatcher = updater.
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.text, text))
    dispatcher.add_handler(MessageHandler(filters.location, location))
    updater.start_polling()
    updater.idle()
