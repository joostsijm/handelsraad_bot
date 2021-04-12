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
    transactions_msgs = ['*Transacties:*', '```']
    for transaction in transactions:
        transactions_msgs.append(
                '{}: {} {}'.format(
                        transaction.id,
                        transaction.date_time.strftime("%Y-%m-%d %H:%M"),
                        transaction.user.name
                    )
            )
        transactions_msgs.append('├ {}'.format(transaction.description))
        index = 1
        for detail in transaction.details:
            transactions_msgs.append(
                    '{}{:>8} {:10} $ {:>9}'.format(
                            '└' if index == len(transaction.details) else '├',
                            str(Value(detail.amount)),
                            ITEMS_INV[detail.item_id],
                            str(Value(detail.money)),
                        )
                )
            index += 1
    transactions_msgs.append('```')
    update.message.reply_text(
            '\n'.join(transactions_msgs), parse_mode=ParseMode.MARKDOWN
        )
