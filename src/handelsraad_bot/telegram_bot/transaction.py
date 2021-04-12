"""Telegram transactions command"""

# pylint: disable=unused-argument

from telegram import ParseMode

from rival_regions_calc import Value

from handelsraad_bot import LOGGER, ITEMS_INV, database


def cmd_transactions(update, context):
    """transactions command"""
    LOGGER.info('%s: CMD transactions', update.message.chat.username)
    executor = database.get_user(update.message.chat.username)
    if 'trader' not in executor.get_roles():
        LOGGER.warning(
                '%s: CMD transactions, not allowed',
                update.message.chat.username
            )
        update.message.reply_text('Benodigde rol voor dit command: trader')
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
