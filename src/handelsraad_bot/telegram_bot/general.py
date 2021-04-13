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
            '/set\\_investment <username> <amount>\n'
            '/transactions <limit>\n'
            '/add\\_transaction',
            parse_mode=ParseMode.MARKDOWN
        )


def cmd_total(update, context):
    """Total command"""
    LOGGER.info('%s: CMD total', update.message.from_user.username)
    if not util.check_permission(
                update, ['trader', 'investor', 'chairman'], 'CMD total'
            ):
        return
    total = database.get_total()
    total_msgs = ['*Totaal:*', '```']
    for resource_id, resource in total.items():
        total_msgs.append(
                '{:10} {:>13} $ {:>5}/1'.format(
                        ITEMS_INV[resource_id],
                        str(Value(resource['amount'])),
                        str(Value(resource['average']))
                    )
            )
    total_msgs.append('```')
    update.message.reply_text(
            '\n'.join(total_msgs), parse_mode=ParseMode.MARKDOWN
        )
