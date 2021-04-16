"""Telegram general commands"""

# pylint: disable=unused-argument

from telegram import ParseMode
from rival_regions_calc import Value

from handelsraad_bot import LOGGER, ITEMS_INV, database, util


def cmd_start(update, context):
    """Start command"""
    update.message.reply_text(
        'Welkom {}, bij de Handelsraad bot. '
        'Gebruik /hulp voor een lijst met commands.'
        .format(
                update.message.from_user.first_name
            )
        )


def cmd_hulp(update, context):
    """Hulp command"""
    update.message.reply_text('Yikes, ik bedoelde eigenlijk /help.')


def cmd_help(update, context):
    """Help command"""
    update.message.reply_text(
            '*Lijst van commands*:\n'
            '/total\n'
            '/limits\n'
            '/set\\_limit <item\\_name> <amount>\n'
            '/remove\\_limit <item\\_nam>\n'
            '/users\n'
            '/set\\_role <username> <role> <boolean>\n'
            '/investors'
            '/set\\_investment <username> <amount>\n'
            '/add\\_transaction\n'
            '/transactions <limit>\n'
            '/remove_transaction <transaction_id>',
            parse_mode=ParseMode.MARKDOWN
        )


def cmd_total(update, context):
    """Total command"""
    LOGGER.info('%s: CMD total', update.message.from_user.username)
    if not util.check_permission(
                update, ['trader', 'investor', 'chairman'], 'CMD total'
            ):
        return
    total = util.get_total()
    total_msgs = ['*Totaal:*', '```']
    total_money = 0
    for item_id, item in total.items():
#        while (len(str(Value(item['amount']))) > 6):
#            m

        total_msgs.append(
                '{:3} $ {:>13} {:>6}/1 {:>13}'.format(
                        ITEMS_INV[item_id][:3],
                        str(Value(item['amount'])),
                        str(Value(item['average'])),
                        str(Value(item['amount'] * item['average']))
                    )
            )
        if item_id:
            total_money += item['amount'] * item['average']
        else:
            total_money += item['amount']
    total_msgs.append('tot $ {:>15}'.format(str(Value(total_money))))
    total_msgs.append('```')
    update.message.reply_text(
            '\n'.join(total_msgs), parse_mode=ParseMode.MARKDOWN
        )
