"""Telegram user commands"""

# pylint: disable=unused-argument

from telegram import ParseMode
from rival_regions_calc import Value

from handelsraad_bot import LOGGER, database, util


def cmd_investors(update, context):
    """List investors"""
    LOGGER.info('%s: CMD investors', update.message.from_user.username)
    if not util.check_permission(
                update, ['trader', 'investor', 'chairman'], 'CMD investors'
            ):
        return
    investors = []
    total = 0
    for investor in database.get_investors():
        investor_dict = {
                'telegram_username': investor.telegram_username,
                'name': investor.name,
                'investment': 0
            }
        investor_dict['investment'] += util.total_investment(investor)
        total += investor_dict['investment']
        investors.append(investor_dict)
    investors_msgs = ['*Investors:*', '```']
    for investor in investors:
        investors_msgs.append('{:10}: $ {:>8}'.format(
                investor['name'],
                str(Value(investor['investment'])),
        ))
    if not investors:
        investors_msgs.append('no investors')
    investors_msgs.append('Totaal    : $ {:>8}'.format(str(Value(total))))
    investors_msgs.append('```')
    update.message.reply_text(
            '\n'.join(investors_msgs), parse_mode=ParseMode.MARKDOWN
        )


def cmd_set_investment(update, context):
    """Set investment"""
    LOGGER.info('%s: CMD set investment', update.message.from_user.username)
    if not util.check_permission(update, ['chairman'], 'CMD set investment'):
        return
    try:
        telegram_username = context.args[0]
        if telegram_username[:1] == '@':
            telegram_username = telegram_username[1:]
    except (IndexError, ValueError):
        LOGGER.warning(
                '%s: CMD set investment, incorrect <investment>',
                update.message.from_user.username,
            )
        update.message.reply_text('Probleem met <username>')
        update.message.reply_text('/set_investment <username> <amount>')
        return

    try:
        amount = Value(context.args[1])
    except (IndexError, ValueError):
        LOGGER.warning(
                '%s: CMD set investment, incorrect <amount>',
                update.message.from_user.username,
            )
        update.message.reply_text('Probleem met <amount>')
        update.message.reply_text('/set_investment <username> <amount>')
        return

    database.set_investment(telegram_username, amount)

    update.message.reply_text(
            'investment set: {} $ {}'.format(telegram_username, amount),
            parse_mode=ParseMode.MARKDOWN
        )
    cmd_investors(update, context)
