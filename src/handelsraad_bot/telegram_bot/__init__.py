"""Telegram bot"""

#pylint: disable=unused-argument

from telegram.ext import CommandHandler

from handelsraad_bot import LOGGER, TELEGRAM_UPDATER

from . import general, limit


def run():
    """run function"""
    LOGGER.info('starting Telegram')

    dispatcher = TELEGRAM_UPDATER.dispatcher

    # general commands
    dispatcher.add_handler(
            CommandHandler('start', general.cmd_start)
        )
    dispatcher.add_handler(
            CommandHandler('help', general.cmd_help)
        )
    dispatcher.add_handler(
            CommandHandler('total', general.cmd_total)
        )

    # limit
    dispatcher.add_handler(
            CommandHandler('limits', limit.cmd_limits)
        )
    dispatcher.add_handler(
            CommandHandler('set_limit', limit.cmd_set_limit)
        )
    dispatcher.add_handler(
            CommandHandler('remove_limit', limit.cmd_remove_limit)
        )

    TELEGRAM_UPDATER.start_polling()
    TELEGRAM_UPDATER.idle()
