"""Telegram transactions command"""

# pylint: disable=unused-argument

from telegram import ParseMode

from rival_regions_calc import Value

from handelsraad_bot import LOGGER, ITEMS, ITEMS_INV, database, util


def cmd_transactions(update, context):
    """transactions command"""
    LOGGER.info('%s: CMD transactions', update.message.from_user.username)
    if not util.check_permission(
                update, ['trader', 'investor', 'chairman'], 'CMD transactions'
            ):
        return
    try:
        limit = int(context.args[0])
    except (IndexError, KeyError):
        limit = 5
    try:
        item_id = ITEMS[context.args[1]]
    except (IndexError, KeyError):
        item_id = None

    transactions = database.get_transactions(limit, item_id)
    transactions_msgs = ['*Transacties:*']
    for transaction in transactions:
        transaction_total = 0
        transactions_msgs.append(
                '*{}*: {} {} ({})'.format(
                        transaction.id,
                        transaction.date_time.strftime("%Y-%m-%d %H:%M"),
                        transaction.user.name,
                        transaction.user.telegram_username,
                    )
            )
        transactions_msgs.append('```')
        transactions_msgs.append('├ {}'.format(transaction.description))
        for detail in transaction.details:
            transactions_msgs.append(
                    '{} {:>14} {:>14}'.format(
                            '├' if len(transaction.details) - 1 else '└',
                            ITEMS_INV[detail.item_id],
                            str(Value(detail.amount)),
                        )
                )
            transactions_msgs.append(
                    '{} $ {:>10}/1 $ {:>12}'.format(
                            '│' if len(transaction.details) - 1 else ' ',
                            str(Value(detail.money / detail.amount)),
                            str(Value(detail.money)),
                        )
                )
            transaction_total += detail.money
        if len(transaction.details) - 1:
            transactions_msgs.append('└         totaal $ {:>12}'.format(
                    str(Value(transaction_total))
                ))
        transactions_msgs.append('```')
    update.message.reply_text(
            '\n'.join(transactions_msgs), parse_mode=ParseMode.MARKDOWN
        )


def cmd_remove_transaction(update, context):
    """remove transaction command"""
    LOGGER.info(
            '%s: CMD remove transaction',
            update.message.from_user.username
        )
    if not util.check_permission(
                update, ['chairman'], 'CMD remove transaction'
            ):
        return
    try:
        transaction_id = int(context.args[0])
    except (ValueError, IndexError):
        LOGGER.warning(
                '%s: CMD remove transaction, incorrect <transaction_id>',
                update.message.from_user.username,
            )
        update.message.reply_text('Probleem met <transaction_id>')
        update.message.reply_text('/remove_transaction <transaction_id>')
        return
    database.remove_transaction(transaction_id)
    update.message.reply_text(
            'Removed transaction {}'.format(transaction_id),
            parse_mode=ParseMode.MARKDOWN
        )
    cmd_transactions(update, context)
