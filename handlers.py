import ephem
import logging
import os
from re import findall
from datetime import datetime

from glob import glob
from random import choice

from telegram import ReplyKeyboardMarkup, KeyboardButton
from utils import get_user_emo, is_cat


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    text = f'Привет {emo}'
    my_keyboard = ReplyKeyboardMarkup([['Прислать котика', 'Сменить аватарку']], resize_keyboard=True)
    # my_keyboard = ReplyKeyboardMarkup([['Прислать котика', 'Сменить аватарку', 'Следующее полнолуние']], resize_keyboard=True)
    update.message.reply_text(text, reply_markup=my_keyboard)


def next_full_moon(bot, update):
    data = update.message.text.split(' ')[1]
    update.message.reply_text(
        f"Следующее полнолуние: {ephem.next_full_moon(data)}")


def wordcount(bot, update):
    text = update.message.text.replace('/wordcount', '')
    pattern = r"\b[a-zA-Zа-я]+\b"
    word_count = len(findall(pattern, text))
    update.message.reply_text("Слов: {} ".format(word_count))


def planet(bot, update):
    planet_name = update.message.text.split(' ')[1]
    planet_list = [name[-1] for name in ephem._libastro.builtin_planets()]
    if planet_name in planet_list:
        planet = getattr(ephem, planet_name)()
        date = datetime.now().strftime('%Y/%m/%d')
        planet.compute(date)
        user_text = (
            f"Планета {planet_name} "
            f"Созвездие: {ephem.constellation(planet)}"
        )
    else:
        user_text = "Введено неверное название планеты"

    update.message.reply_text(user_text)


def talk_to_me(bot, update):
    user_text = (
        f"Привет {update.message.chat.first_name}! "
        f"Ты написал: {update.message.text}"
    )
    logging.info(
        f"User: {update.message.chat.username} "
        f"Chat id: {update.message.chat.id} "
        f"Message: {update.message.text}"
       )
    print(update.message)
    update.message.reply_text(user_text)


def send_cat_picture(bot, update):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text(f'Готово {emo}')


def check_user_photo(bot, update, user_data):
    update.message.reply_text("Обрабатываю фото")
    os.makedirs('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join(f'downloads', '{photo_file.file_id}.jpg')
    photo_file.download(filename)
    if is_cat(filename):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку.")
        new_filename = os.path.join(f'images', 'cat_{photo_file.file_id}.jpg')
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Котика нет")
