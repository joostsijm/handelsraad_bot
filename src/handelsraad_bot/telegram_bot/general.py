"""Telegram general commands"""

#pylint: disable=unused-argument

from telegram import ParseMode

from rival_regions_calc import Value

from handelsraad_bot import LOGGER, ITEMS_INV, database


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
    total = database.get_total()
    total_msgs = ['**Total**']
    for resource_id, total in total.items():
        total_msgs.append(
                '{:8}, {}'.format(
                        ITEMS_INV[resource_id],
                        Value(total)
                    )
            )
    update.message.reply_text(
            '\n'.join(total_msgs), parse_mode=ParseMode.MARKDOWN
        )
