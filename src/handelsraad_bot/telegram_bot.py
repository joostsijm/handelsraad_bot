"""Telegram bot"""

#pylint: disable=unused-argument

from telegram import ParseMode
from telegram.ext import CommandHandler

from handelsraad_bot import LOGGER, TELEGRAM_UPDATER, STATE_ITEMS, \
        STATE_ITEMS_INV, database


def cmd_start(update, context):
    """Start command"""
    update.message.reply_text(
        'Hi {}'.format(update.message.from_user.first_name))


def cmd_help(update, context):
    """Help command"""
    update.message.reply_text('**HELP**', parse_mode=ParseMode.MARKDOWN)


def cmd_total(update, context):
    """Total command"""
    totals = database.get_totals()
    totals_msgs = ['**Total**']
    for resource_id, total in totals.items():
        totals_msgs.append('{:8}, {}'.format(
                STATE_ITEMS_INV[resource_id], total)
            )
    update.message.reply_text(
            '\n'.join(totals_msgs), parse_mode=ParseMode.MARKDOWN
        )


def cmd_limits(update, context):
    """limits command"""
    limits = database.get_limits()
    limits_msgs = ['**Limits**']
    for resource_id, limit in limits.items():
        limits_msgs.append('{:8}: {}'.format(
                STATE_ITEMS_INV[resource_id], limit)
            )
    update.message.reply_text(
            '\n'.join(limits_msgs), parse_mode=ParseMode.MARKDOWN
        )


def cmd_set_limit(update, context):
    """Set limit"""
    try:
        item_name = context.args[0]
    except IndexError:
        LOGGER.info('No item name given')
        update.message.reply_text('/set_limit <item_name> <amount>')
        update.message.reply_text('No item name given')
        return

    try:
        item_id = STATE_ITEMS[item_name]
    except IndexError:
        LOGGER.info('Item name not found')
        update.message.reply_text('/set_limit <item_name> <amount>')
        update.message.reply_text('Item name not found')
        return

    try:
        amount = context.args[1]
    except IndexError:
        LOGGER.info('No amount given')
        update.message.reply_text('/set_limit <item_name> <amount>')
        update.message.reply_text('No amount given')
        return

    try:
        amount = int(amount)
    except IndexError:
        LOGGER.info('Ammount is not an int')
        update.message.reply_text('/set_limit <item_name> <amount>')
        update.message.reply_text('Ammount is not an int')
        return

    database.set_limit(item_id, amount)

    update.message.reply_text(
            'Limit created: {} {}'.format(item_name, amount),
            parse_mode=ParseMode.MARKDOWN
        )


def cmd_remove_limit(update, context):
    """Set limit"""
    try:
        item_name = context.args[0]
    except IndexError:
        LOGGER.info('No item name given')
        update.message.reply_text('/remove_limit <item_name>')
        update.message.reply_text('No item name given')
        return

    try:
        item_id = STATE_ITEMS[item_name]
    except IndexError:
        LOGGER.info('Item name not found')
        update.message.reply_text('/remove_limit <item_name>')
        update.message.reply_text('Item name not found')
        return

    database.remove_limit(item_id)

    update.message.reply_text(
            'Limit removed: {}'.format(item_name),
            parse_mode=ParseMode.MARKDOWN
        )

def run():
    """run function"""
    LOGGER.info('starting Telegram')

    dispatcher = TELEGRAM_UPDATER.dispatcher

    # general commands
    dispatcher.add_handler(CommandHandler('start', cmd_start))
    dispatcher.add_handler(CommandHandler('help', cmd_help))

    # handelsraad
    dispatcher.add_handler(CommandHandler('total', cmd_total))
    dispatcher.add_handler(CommandHandler('limits', cmd_limits))
    dispatcher.add_handler(CommandHandler('set_limit', cmd_set_limit))
    dispatcher.add_handler(CommandHandler('remove_limit', cmd_remove_limit))

    TELEGRAM_UPDATER.start_polling()
    TELEGRAM_UPDATER.idle()
