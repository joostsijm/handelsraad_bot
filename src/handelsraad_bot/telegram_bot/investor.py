"""Telegram user commands"""

# pylint: disable=unused-argument

from telegram import ParseMode
from rival_regions_calc import Value

from handelsraad_bot import LOGGER, database


def cmd_investors(update, context):
    """List investors"""
    LOGGER.info('%s: CMD investors', update.message.chat.username)
    investors = []
    total = 0
    for investor in database.get_investors():
        investor_dict = {
                'telegram_username': investor.telegram_username,
                'name': investor.name,
                'investment': 0
            }
        for investment in investor.investments:
            investor_dict['investment'] += investment.amount
            total += investment.amount
        investors.append(investor_dict)
    investors_msgs = ['**Investors:**']
    for investor in investors:
        investors_msgs.append('{}: $ {:>8}'.format(
                investor['name'],
                str(Value(investor['investment'])),
        ))
    if not investors:
        investors_msgs.append('no investors')
    investors_msgs.append('totaal: $ {:>8}'.format(str(Value(total))))
    update.message.reply_text(
            '\n'.join(investors_msgs), parse_mode=ParseMode.MARKDOWN
        )


def cmd_set_investment(update, context):
    """Set investment"""
    LOGGER.info('%s: CMD set investment', update.message.chat.username)
    try:
        telegram_username = context.args[0]
        if telegram_username[:1] == '@':
            telegram_username = telegram_username[1:]
    except (IndexError, ValueError):
        LOGGER.warning(
                '%s: CMD set investment, incorrect <investment>',
                update.message.chat.username,
            )
        update.message.reply_text('Probleem met <username>')
        update.message.reply_text('/set_investment <username> <amount>')
        return

    try:
        amount = Value(context.args[1])
    except (IndexError, ValueError):
        LOGGER.warning(
                '%s: CMD set investment, incorrect <amount>',
                update.message.chat.username,
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
