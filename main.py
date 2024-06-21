# First of all, you need to register and get a subscription to this api:
# https://probivapi.com/

from aiogram import Bot, Dispatcher, executor, types
import requests
import json

# Telegram bot token
API_TOKEN = "6936366913:AAFSg1r7cxJp4WuOqv-byMvhevjC_pvqS0o"

# ProbivAPI secret key
PROBIVAPI_KEY = "9b4030a1-d8a7-4d0c-adbc-d5dd701dac70"

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
    url = "https://probivapi.com/api/phone/info/" + nomer

    # Necessary headers for the API to work
    head = {
        # API key that you can get by subscribing to the API
        "X-Auth": PROBIVAPI_KEY
    }

    # Send the request with all the parameters and print the result for debugging
    response = requests.get(url, headers=head)
    print(response.text)

    # Load the data of the response into a JSON object
    try:
        json_response = response.json()
    except Exception:
        json_response = {}

    # Catch errors depending on the response
    # Integrated TrueCaller API
    try:
        truecaller_api_name = str(json_response['truecaller']['data'][0]['name'])
    except Exception:
        truecaller_api_name = 'Not found'
    # Integrated Numbuster API
    try:
        numbuster_api_name = str(json_response['numbuster']['averageProfile']['firstName']) + \
        str(json_response['numbuster']['averageProfile']['lastName'])
    except Exception:
        numbuster_api_name = 'Not found'
    # Integrated EyeCon API
    try:
        eyecon_api_name = str(json_response['eyecon'])
    except Exception:
        eyecon_api_name = 'Not found'
    # Integrated ViewCaller API
    try:
        viewcaller_name_list = []
        for tag in json_response['viewcaller']:
            viewcaller_name_list.append(tag['name'])
        viewcaller_api_name = ', '.join(viewcaller_name_list)
    except Exception:
        viewcaller_api_name = 'Not found'

    # Send the formatted data to the user on Telegram
    await bot.send_message(message.chat.id,f"""
                           
                           📱 ФИО (Numbuster): {numbuster_api_name}
                           🌐 ФИО (EyeCon): {eyecon_api_name}
                           🔎 ФИО (ViewCaller): {viewcaller_api_name}
                           📞 ФИО (TrueCaller): {truecaller_api_name}

                           @dimondev_ru
                           
                           Код бота: https://github.com/SegYT/glazboga/

                           Пробив API: https://probivapi.com
                           """)


# Main loop
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
