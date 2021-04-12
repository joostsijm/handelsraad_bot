"""Telegram transactions command"""

# pylint: disable=unused-argument

from telegram import ParseMode

from rival_regions_calc import Value

from handelsraad_bot import LOGGER, ITEMS_INV, database, util


def cmd_transactions(update, context):
    """transactions command"""
    LOGGER.info('%s: CMD transactions', update.message.chat.username)
    if not util.check_permission(
                update, ['trader', 'investor', 'chairman'], 'CMD transactions'
            ):
        return
    transactions = database.get_transactions()
    transactions_msgs = ['**Transactions:**']
    for transaction in transactions:
        transactions_msgs.append(
                '{}: {}'.format(
                        transaction.id,
                        transaction.description
                    )
            )
        for detail in transaction.details:
            transactions_msgs.append(
                    '{:8}: {} $ {}'.format(
                            ITEMS_INV[detail.item_id],
                            Value(detail.amount),
                            Value(detail.money),
                        )
                )
    update.message.reply_text(
            '\n'.join(transactions_msgs), parse_mode=ParseMode.MARKDOWN
        )
