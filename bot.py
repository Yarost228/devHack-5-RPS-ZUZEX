from telebot import *
import json
import os
import numpy as np
from tensorflow.keras.models import load_model
import cv2

from random import *

MODEL_PATH = "/content/drive/MyDrive/model/NeyronchikBeter.h5" # это надо поменять на директорию с нейронкой, щас оно настроено на Google Drive для работы на Google Colab



unique_labels = ["paper", "rock", "scissors"]
model = load_model(MODEL_PATH)


bot = telebot.TeleBot('7932251208:AAHaoaBKRcVQQKxXAA2on9DfYeiKFJI-KC0')

def process_image(image):
    image = image.resize((64, 64))
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0)

def roll_rps(vvod, message):
    rps = ["rock", "paper", "scissors"]
    if rps.count(vvod) != 0:
        vibor = choice(rps)
        bot.send_message(message.chat.id, "Выбор оппонента: " + vibor, parse_mode='html')
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
    with open(f'/content/drive/MyDrive/users/{message.from_user.username}.json', 'w+') as file: # здесь также необходимо менять код если запуск не на колабе
        json.dump(statlist, file)


def getStats(message):
    with open(f'/content/drive/MyDrive/users/{message.from_user.username}.json', 'r') as file: # здесь также необходимо менять код если запуск не на колабе
        return json.load(file)


@bot.message_handler(commands=['start'])
def startBot(message):
    bot.send_message(message.chat.id, "Отправьте фото вашего выбора.", parse_mode='html')
    writeStats(message, [0, 0, 0])

@bot.message_handler(content_types=['photo'])
def checkImage(message):
    if message.photo:
        # Получение самого большого по размеру изображения
        photo = message.photo[-1]

        # Загрузка файла
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = 'photo.jpg'
        with open(save_path, 'wb') as new_file:
          new_file.write(downloaded_file)

        # Предобработка изображения
        image = cv2.imread(save_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (64, 64))  # Используйте размер из вашей модели
        image = image / 255.0
        image = np.expand_dims(image, axis=0)

        # Предсказание
        predictions = model.predict(image)
        predicted_label = unique_labels[np.argmax(predictions)]

        # Ответ пользователю
        bot.send_message(message.chat.id, f'Распознанный жест: {predicted_label}', parse_mode='html')

        # Удаление сохранённого изображения
        os.remove(save_path)
        roll = roll_rps(predicted_label, message)
        w, l, t = getStats(message)[0], getStats(message)[1], getStats(message)[2]
        if roll == "you win":
            writeStats(message, [int(w) + 1, l, t])
            roll = "Вы выиграли!"
        if roll == "you lose":
            writeStats(message, [w, int(l) + 1, t])
            roll = "Вы проиграли!"
        if roll == "tie":
            writeStats(message, [w, l, int(t) + 1])
            roll = "Ничья."
        bot.send_message(message.chat.id, roll, parse_mode='html')
        bot.send_message(message.chat.id, "введите rock, paper или scissors", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Отправьте фото вашего выбора.", parse_mode='html')


@bot.message_handler(commands=['leaderboard'])
def showLeaderboard(message):
    directory = f"/content/drive/MyDrive/users" # здесь также необходимо менять код если запуск не на колабе
    leaderboard = {}
    text = ""
    files = os.listdir(directory)
    for user in files:
        with open(f'/content/drive/MyDrive/users/{user}', 'r') as file: # здесь также необходимо менять код если запуск не на колабе
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
        roll = "Вы выиграли!"
    if roll == "you lose":
        writeStats(message, [w, int(l) + 1, t])
        roll = "Вы проиграли!"
    if roll == "tie":
        writeStats(message, [w, l, int(t) + 1])
        roll = "Ничья."
    bot.send_message(message.chat.id, roll, parse_mode='html')
    bot.send_message(message.chat.id, "Введите rock, paper или scissors.", parse_mode='html')


bot.polling(none_stop=True)