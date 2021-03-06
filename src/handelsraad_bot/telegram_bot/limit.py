"""Telegram limit commands"""

# pylint: disable=unused-argument

from telegram import ParseMode
from rival_regions_calc import Value

from handelsraad_bot import LOGGER, ITEMS, ITEMS_INV, database, util


def cmd_limits(update, context):
    """limits command"""
    LOGGER.info('%s: CMD limits', update.message.from_user.username)
    if not util.check_permission(
                update, ['trader', 'investor', 'chairman'], 'CMD limits'
            ):
        return
    limits = database.get_limits()
    limits_msgs = ['*Limieten:*', '```']
    for resource_id, limit in limits.items():
        limits_msgs.append('{:10}: {:>9}'.format(
                ITEMS_INV[resource_id],
                str(Value(limit))
            ))
    if not limits:
        limits_msgs.append('no limits')
    limits_msgs.append('```')
    update.message.reply_text(
            '\n'.join(limits_msgs), parse_mode=ParseMode.MARKDOWN
        )


def cmd_set(update, context):
    """Set limit"""
    LOGGER.info('%s: CMD set limit', update.message.from_user.username)
    if not util.check_permission(update, ['chairman'], 'CMD set limit'):
        return
    try:
        item_name = context.args[0]
    except IndexError:
        LOGGER.info('No item name given')
        update.message.reply_text('/set_limit <item_name> <amount>')
        update.message.reply_text('No item name given')
        return

    try:
        item_id = ITEMS[item_name]
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


def cmd_remove(update, context):
    """Set limit"""
    LOGGER.info('%s: CMD remove limit', update.message.from_user.username)
    if not util.check_permission(update, ['chairman'], 'CMD remove limit'):
        return
    try:
        item_name = context.args[0]
    except IndexError:
        LOGGER.info('No item name given')
        update.message.reply_text('/remove_limit <item_name>')
        update.message.reply_text('No item name given')
        return

    try:
        item_id = ITEMS[item_name]
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
