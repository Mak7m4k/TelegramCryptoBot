import telebot
from requests import Session


TOKEN = '5869011389:'
bot = telebot.TeleBot(TOKEN)

headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '',
        }

WelcomeMessage = '''Привет! Я Бот для работы с криптовалютой.
Я использую API coinmarketcap и могу работать только с теми валютами, которые там размещены.
    Инфо (валюта) - выдаёт информацию о валюте
    Курс (валюта) (2валюта) - выдаёт текущий курс
Пример:
    Инфо BTC
    Курс BTC RUB
Создатель: @Mak7m4k
'''


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, WelcomeMessage)


@bot.message_handler(func=lambda message: True)
def crypto(message):
    text = message.text.split()
    if text[0] == 'Инфо':
        try:
            url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
            parameters = {'symbol': str(text[1])}

            session = Session()
            session.headers.update(headers)
            response = session.get(url, params=parameters)
            data = str(response.json()['data'][str(text[1])][0])
            data = data.replace("'", '').replace("{", '').replace("}", '').split(', ')
            vault_name = data[1].split(': ')[1]
            vault_symbol = data[2].split(': ')[1]
            vault_logo = data[6].split(': ')[1]
            vault_website = None
            for i in data:
                if 'website:' in i:
                    vault_website = i.split(' ')[2].replace('[', '').replace(']', '')

            answer = f'Название: {vault_name}\n' \
                     f'Обозначение: {vault_symbol}\n' \
                     f'Сайт: {vault_website}\n' \
                     f''

            bot.send_photo(message.chat.id, vault_logo, answer)
        except:
            bot.send_message(message.chat.id, 'Произошла ошибка. Проверьте написание валюты.\nВозможно такой валюты не существует.')
    elif text[0] == 'Курс':
        try:
            url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
            parameters = {
                'amount': '1',
                'symbol': str(text[1]),
                'convert': str(text[2])
            }

            session = Session()
            session.headers.update(headers)
            response = session.get(url, params=parameters)
            data = str(response.json()['data'][0])
            data = data.replace("'", '').replace("{", '').replace("}", '').split(',')
            vault_symbol = data[1].split(': ')[1]
            vault_prise = data[5].split(': ')[3]
            vault2_symbol = data[5].split(': ')[1]

            bot.send_message(message.chat.id, f'1 {vault_symbol} = {vault_prise} {vault2_symbol}')
        except:
            bot.send_message(message.chat.id, f'Произошла ошибка. Проверьте написание валют.')
    else:
        bot.send_message(message.chat.id, f'Неизвестная команда.')


bot.infinity_polling()
