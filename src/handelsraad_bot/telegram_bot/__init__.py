"""Telegram bot"""

# pylint: disable=unused-argument

from telegram.ext import CommandHandler

from handelsraad_bot import LOGGER, TELEGRAM_UPDATER

from . import general, limit, transaction, add_transaction, user, investor


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
            CommandHandler('set_limit', limit.cmd_set)
        )
    dispatcher.add_handler(
            CommandHandler('remove_limit', limit.cmd_remove)
        )

    # user
    dispatcher.add_handler(
            CommandHandler('users', user.cmd_users)
        )
    dispatcher.add_handler(
            CommandHandler('set_role', user.cmd_set_role)
        )

    # investor
    dispatcher.add_handler(
            CommandHandler('investors', investor.cmd_investors)
        )
    dispatcher.add_handler(
            CommandHandler('set_investment', investor.cmd_set_investment)
        )

    # transaction
    dispatcher.add_handler(
            CommandHandler('transactions', transaction.cmd_transactions)
        )
    dispatcher.add_handler(
            add_transaction.conversation
        )

    TELEGRAM_UPDATER.start_polling()
    TELEGRAM_UPDATER.idle()
