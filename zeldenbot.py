import ephem
from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup

import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запустился')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('planet', planet))
    dp.add_handler(CommandHandler('wordcount', wordcount))
    dp.add_handler(CommandHandler('moon', next_full_moon))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))


    mybot.start_polling()
    mybot.idle()

def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text(f'Готово {emo}')
    
def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    #user_data['emo'] = emo
    text = f'Привет {emo}'
    my_keyboard = ReplyKeyboardMarkup([['Прислать котика', 'Сменить аватарку']], resize_keyboard=True)
    update.message.reply_text(text, reply_markup=my_keyboard)


def next_full_moon(bot, update):
    data = update.message.text.split(' ')[1]
    update.message.reply_text(
        f"Следующее полнолуние: {ephem.next_full_moon(data)}")


def wordcount(bot, update):
    text = update.message.text.replace('/wordcount', '')
    word_list = text.split()
    filtered_list = list(filter(str_filter, word_list))
    word_count = len(filtered_list)
    update.message.reply_text("Слов: {} ".format(word_count))


def str_filter(x):
    if x.isalpha():
        return 1
    else:
        return 0


def planet(bot, update):
    planet_name = update.message.text.split(' ')[1]
    planet_list = [name[-1] for name in ephem._libastro.builtin_planets()]
    if planet_name in planet_list:
        a = getattr(ephem, planet_name)()
        a.compute('2019/5/24')
        user_text = (
            f"Планета {planet_name} "
            f"Созвездие: {ephem.constellation(a)}"
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
        'User: %s, Chat id: %s, Message: %s',
        update.message.chat.username,
        update.message.chat.id, update.message.text)
    print(update.message)
    update.message.reply_text(user_text)

def send_cat_picture(bot, update):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))

def send_cat_picture2(bot, update):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))

main()
