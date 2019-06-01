from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

from handlers import greet_user, talk_to_me, send_cat_picture, change_avatar, planet, next_full_moon, wordcount, check_user_photo
import logging
import settings


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запустился')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('planet', planet))
    dp.add_handler(CommandHandler('wordcount', wordcount))
    # dp.add_handler(RegexHandler('^(Следующее полнолуние)$', next_full_moon))
    dp.add_handler(CommandHandler('moon', next_full_moon))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
