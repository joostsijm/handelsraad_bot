"""Telegram limit commands"""

#pylint: disable=unused-argument

from telegram import ParseMode

from handelsraad_bot import LOGGER, STATE_ITEMS, \
        STATE_ITEMS_INV, database


def cmd_limits(update, context):
    """limits command"""
    LOGGER.info('%s: CMD limits', update.message.chat.username)
    limits = database.get_limits()
    limits_msgs = ['**Limits:**']
    for resource_id, limit in limits.items():
        limits_msgs.append('{:8}: {}'.format(
                STATE_ITEMS_INV[resource_id], limit)
            )
    if not limits:
        limits_msgs.append('no limits')
    update.message.reply_text(
            '\n'.join(limits_msgs), parse_mode=ParseMode.MARKDOWN
        )


def cmd_set_limit(update, context):
    """Set limit"""
    LOGGER.info('%s: CMD set limit', update.message.chat.username)
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
    LOGGER.info('%s: CMD remove limit', update.message.chat.username)
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
