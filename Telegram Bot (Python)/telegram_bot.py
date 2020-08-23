#pip install requests
import requests

#pip3 install python-telegram-bot
from telegram.ext import Updater, CommandHandler





### MAIN Function ###


# response = requests.get("https://api.telegram.org/bot1115939597:AAFJr-WpQz96yJ_ulJXwNApv_q32WuMg2Jk/getMe", 'Content-Type:application/json; charset=utf-8')

# print (response)
# print (response.text)
# print (response.encoding)
# print (response.raise_for_status())
# print (response.status_code)
# print (response.history)





def hi (bot, update):
    
    chat_id = update.message.chat_id
    bot.send_message(chat_id, "Hi")

def main():
    updater = Updater('1115939597:AAFJr-WpQz96yJ_ulJXwNApv_q32WuMg2Jk')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('hi',hi))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()