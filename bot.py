from telebot import *
from telebot import types


from random import *

bot = telebot.TeleBot('7932251208:AAHaoaBKRcVQQKxXAA2on9DfYeiKFJI-KC0')

def roll_rps(vvod, message):
    rps = ["rock", "paper", "scissors"]
    if rps.count(vvod) != 0:
        vibor = choice(rps)
        bot.send_message(message.chat.id, vibor, parse_mode='html')
        if vibor == vvod:
            return "tie"

        elif vibor == "rock":
            if vvod == "scissors":
                return "you lose"
            elif vvod == "paper":
                return "you win"

        elif vibor == "paper":
            if vvod == "scissors":
                return "you win"
            elif vvod == "rock":
                return "you lose"

        elif vibor == "scissors":
            if vvod == "rock":
                return "you win"
            elif vvod == "paper":
                return "you lose"

    else:
        return "unknown"


@bot.message_handler(commands=['start'])
def startBot(message):
    bot.send_message(message.chat.id, "введите rock, paper или scissors", parse_mode='html')

@bot.message_handler(content_types=['text'])
def phrase(message):
    bot.send_message(message.chat.id, roll_rps(message.text, message), parse_mode='html')

bot.polling(none_stop=True)