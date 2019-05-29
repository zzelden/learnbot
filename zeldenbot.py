from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import ephem

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запустился')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet))
    dp.add_handler(CommandHandler('wordcount', wordcount))
    dp.add_handler(CommandHandler('moon', next_full_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


def greet_user(bot, update):
    text = ('Вызван /start')
    print(text)
    update.message.reply_text(text)


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


main()
