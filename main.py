import telebot
from currency_converter import CurrencyConverter
from telebot import types


bot = telebot.TeleBot('5616406717:AAH6_2K-qRibskZEriBE8T_0hbUzq2Qsxmo')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Hello write summ')
    bot.register_next_step_handler(message,summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id,'No true format message')
        bot.register_next_step_handler(message,summa)
        return


    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR',callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GPB', callback_data='usd/gpb')
        btn4 = types.InlineKeyboardButton('Diferent', callback_data='else')
        markup.add(btn1,btn2,btn3,btn4)
        bot.send_message(message.chat.id,'Chose couple value',reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'No true format message.Write > 0')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount,values[0],values[1])
        bot.send_message(call.message.chat.id,f'Total:{round(res,2)}.If you would like write summa repite - write')
        bot.register_next_step_handler(call.message,summa)
    else:
        bot.send_message(call.message.chat.id,'Write valur across /')
        bot.register_next_step_handler(call.message,my_currency)

def my_currency(message):
    try:
        values = message.text.uppper().split('/')
        res = currency.convert(amount,values[0],values[1])
        bot.send_message(message.chat.id,f'Total:{round(res,2)}.If you would like write summa repite - write')
        bot.register_next_step_handler(message,summa)
    except Exception:
        bot.send_message(message.chat.id, 'Ooops, I have problem. Write agine')
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop=True)