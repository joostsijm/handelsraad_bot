"""Telegram bot"""

from telegram import ParseMode
from telegram.ext import CommandHandler

from handelsraad_bot import TELEGRAM_UPDATER


def cmd_start(update, context):
    """Start command"""
    update.message.reply_text(
        'Hi {}'.format(update.message.from_user.first_name))

def cmd_help(update, context):
    """Help command"""
    update.message.reply_text('**HELP**', parse_mode=ParseMode.MARKDOWN)

def run():
    """run function"""

    dispatcher = TELEGRAM_UPDATER.dispatcher

    # general commands
    dispatcher.add_handler(CommandHandler('start', cmd_start))
    dispatcher.add_handler(CommandHandler('help', cmd_help))

    TELEGRAM_UPDATER.start_polling()
    TELEGRAM_UPDATER.idle()
