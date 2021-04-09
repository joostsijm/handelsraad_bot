"""Telegram general commands"""

#pylint: disable=unused-argument

from telegram import ParseMode

from handelsraad_bot import LOGGER, STATE_ITEMS_INV, database


def cmd_start(update, context):
    """Start command"""
    update.message.reply_text(
        'Hi {}'.format(update.message.from_user.first_name))


def cmd_help(update, context):
    """Help command"""
    update.message.reply_text('**HELP**', parse_mode=ParseMode.MARKDOWN)


def cmd_total(update, context):
    """Total command"""
    LOGGER.info('%s: CMD total', update.message.chat.username)
    totals = database.get_totals()
    totals_msgs = ['**Total**']
    for resource_id, total in totals.items():
        totals_msgs.append('{:8}, {}'.format(
                STATE_ITEMS_INV[resource_id], total)
            )
    update.message.reply_text(
            '\n'.join(totals_msgs), parse_mode=ParseMode.MARKDOWN
        )
