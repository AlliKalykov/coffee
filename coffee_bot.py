import telebot
import logging
from telebot import types
from config import token

TOKEN = token

bot = telebot.TeleBot(TOKEN)

main_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button1 = types.KeyboardButton(text='/start')
button2 = types.KeyboardButton(text='/coffee')
main_keyboard.add(button1, button2)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Хотите насладиться кофе, нажмите на кнопку /coffee', reply_markup=main_keyboard)

@bot.message_handler(commands=['coffee'])
def coffee(message):
    bot.send_message(message.chat.id, 'Какой кофе вы хотите?')
    bot.register_next_step_handler(message, choice_coffee)

def choice_coffee(message):
    order = {
        'coffee': message.text
    }
    size_keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    button1 = types.KeyboardButton(text='Маленький')
    button2 = types.KeyboardButton(text='Средний')
    button3 = types.KeyboardButton(text='Большой')
    size_keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id, 'Какой размер вы хотите?', reply_markup=size_keyboard)
    bot.register_next_step_handler(message, choice_size, order)

def choice_size(message, order):
    order['size'] = message.text
    bot.send_message(message.chat.id, 'На каком молоке вы хотите?', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, choice_milk, order)

def choice_milk(message, order):
    order['milk'] = message.text
    bot.send_message(message.chat.id, f"Ваш заказ: {order['coffee']} {order['size']} {order['milk']}")
    bot.send_message(477072660, f"Пользователь: @{message.from_user.username} \nВаш заказ: {order['coffee']} {order['size']} {order['milk']}")

if __name__ == '__main__':
    print('Start polling...')
    bot.polling(none_stop=True)


