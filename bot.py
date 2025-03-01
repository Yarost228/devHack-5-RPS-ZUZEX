from telebot import *
import json
import os

from random import *

counts = [0, 0, 0]

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

def writeStats(message, statlist):
    with open(f'users/{message.from_user.username}.json', 'w+') as file:
        json.dump(statlist, file)


def getStats(message):
    with open(f'users/{message.from_user.username}.json', 'r') as file:
        return json.load(file)


@bot.message_handler(commands=['start'])
def startBot(message):
    bot.send_message(message.chat.id, "введите rock, paper или scissors", parse_mode='html')
    writeStats(message, [0, 0, 0])

@bot.message_handler(commands=['leaderboard'])
def showLeaderboard(message):
    directory = f"{os.curdir}/users"
    leaderboard = {}
    text = ""
    files = os.listdir(directory)
    for user in files:
        with open(f'users/{user}', 'r') as file:
            leaderboard[user] = json.load(file)[0]
    sortedLeaderboard = sorted(leaderboard.items(), key=lambda leader: leader[1], reverse=True)
    for user in sortedLeaderboard:
        text += f"{user[0].replace('.json', '')}: {user[1]}\n"
    bot.send_message(message.chat.id, text, parse_mode='html')

@bot.message_handler(commands=['stats'])
def showStats(message):
    bot.send_message(message.chat.id, f"w {getStats(message)[0]}, l {getStats(message)[1]}, t {getStats(message)[2]}", parse_mode='html')

@bot.message_handler(content_types=['text'])
def phrase(message):
    roll = roll_rps(message.text.lower(), message)
    w, l, t = getStats(message)[0], getStats(message)[1], getStats(message)[2]
    if roll == "you win":
        writeStats(message, [int(w) + 1, l, t])
    if roll == "you lose":
        writeStats(message, [w, int(l) + 1, t])
    if roll == "tie":
        writeStats(message, [w, l, int(t) + 1])
    bot.send_message(message.chat.id, roll, parse_mode='html')
    bot.send_message(message.chat.id, "введите rock, paper или scissors", parse_mode='html')


bot.polling(none_stop=True)