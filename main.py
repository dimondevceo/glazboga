# First of all, you need to register and get a subscription to this api:
# https://rapidapi.com/segnayt-e1RorVbq3qe/api/dimondevosint/

import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
import json

# Telegram bot token
API_TOKEN = "___TELEGRAM_API_TOKEN___"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

print("!BOT STARTED!")

# Message handler that sends greeting when bot started
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Probiv Bot Template by DimonDev: @dimondevchat")


# This is the main probiv function that returns a json and formats it, then sends it
@dp.message_handler(content_types=['text'])
async def text(message: types.Message):

    # Get the message text and interpret it as a phone number
    nomer = message.text
    print(nomer)

    # The endpoint for the probiv API that passes as a query the phone number
    url = "https://dimondevosint.p.rapidapi.com/main?phone=" + nomer

    # Necessary headers for the API to work
    head = {
        # RapidAPI necessary host header
        "X-RapidAPI-Host": "dimondevosint.p.rapidapi.com",
        # API key that you can get by subscribing to the API
        "X-RapidAPI-Key": "___RAPIDAPI_API_KEY___"
    }

    # Send the request with all the parameters and print the result for debugging
    response = requests.request("GET", url, headers=head)
    print(response.text)

    # Load the data of the response into a JSON object
    data = json.loads(response.text)

    # Send the formatted data to the user on Telegram
    await bot.send_message(message.chat.id,f"""
                           
                           👨 ФИО: {data['name']}
                           🏳️ Страна: {data['country']}
                           📱 Оператор: {data['operator']}
                           📓 Объявления: {data['obyavleniya']}

                           @dimondevchat
                           
                           Код бота: https://github.com/SegYT/glazboga/
                           """)


# Main loop
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
