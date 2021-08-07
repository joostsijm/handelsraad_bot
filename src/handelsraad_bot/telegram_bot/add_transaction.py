"""Telegram transactions command"""

# pylint: disable=unused-argument

from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, \
        ConversationHandler
from rival_regions_calc import Value

from handelsraad_bot import LOGGER, ITEMS, ITEMS_INV, database, util
from handelsraad_bot.telegram_bot import transaction


INSTRUCTIONS = """```
/sell <item> <amount> <price_each>
/buy <item> <amount> <price_each>
/add <item> <amount> <money>
```
bijvoorbeeld:
```
/sell uranium 1kk 2000
/add uranium 1kk 2kkk
/buy oil 10kkk 190
/add oil 10kkk -1900kkk```"""


def print_transaction(update, context):
    """Print transaction"""
    index = 1
    total_money = 0
    transaction_msg = [
            'Transaction omschrijving: "{}"'.format(
                    context.user_data['transaction']['description']
                ),
            'Details:',
            '```',
            ]
    for detail in context.user_data['transaction']['details']:
        transaction_msg.append(
                '{}: {:>8} {:10} $ {:>8}'.format(
                        index,
                        str(detail['amount']),
                        ITEMS_INV[detail['item_id']],
                        str(detail['money'])
                    )
            )
        index += 1
        total_money += detail['money']

    transaction_msg.append('```')
    transaction_msg.append('Totaal geld: $ {}'.format(Value(total_money)))

    update.message.reply_text(
            '\n'.join(transaction_msg),
            parse_mode=ParseMode.MARKDOWN
        )


def conv_transaction_start(update, context):
    """Start message"""
    LOGGER.info(
            '%s: CONV add_transaction, CMD start',
            update.message.from_user.username
        )
    if not util.check_permission(
                update, ['trader', 'chairman'], 'CONV add_transaction'
            ):
        return ConversationHandler.END
    update.message.reply_text('Stuur de beschrijving voor transactie:')

    return TRANSACTION


def conv_transaction_ask_details(update, context):
    """Transaction ask details"""
    LOGGER.info(
            '%s: CONV add_transaction, description: "%s"',
            update.message.from_user.username,
            update.message.text
        )
    context.user_data['transaction'] = {
            'telegram_username': update.message.from_user.username,
            'telegram_id': update.message.from_user.id,
            'description': update.message.text,
            'details': [],
        }
    update.message.reply_text(
            'Voeg transactie details toe.\n' + INSTRUCTIONS,
            parse_mode=ParseMode.MARKDOWN
        )

    return DETAIL


def conv_transaction_detail_add(update, context):
    """Add transaction detail"""
    command = update.message.text.split(' ')[0]
    LOGGER.info(
            '%s: CONV add_transaction, CMD %s',
            update.message.from_user.username,
            command
        )
    try:
        item_id = ITEMS[context.args[0]]
    except (IndexError, KeyError):
        LOGGER.warning(
                '%s: CONV add_transaction, CMD %s, incorrect item name',
                update.message.from_user.username,
                command
            )
        update.message.reply_text('Probleem met <name>.')
        update.message.reply_text(
                '{} <item> <amount> <price_each>'.format(command)
            )
        return DETAIL

    try:
        if command == '/sell':
            amount = Value(-abs(Value(context.args[1])))
        elif command == '/buy':
            amount = Value(abs(Value(context.args[1])))
    except (IndexError, ValueError):
        LOGGER.warning(
                '%s: CONV add_transaction, CMD %s, incorrect amount',
                update.message.from_user.username,
                command
            )
        update.message.reply_text('Probleem met <amount>.')
        update.message.reply_text(
                '{} <item> <amount> <price_each>'.format(command)
            )
        return DETAIL

    try:
        price = Value(context.args[2])
    except (IndexError, ValueError):
        LOGGER.warning(
                '%s: CONV add_transaction, CMD %s, incorrect price each',
                update.message.from_user.username,
                command
            )
        update.message.reply_text('Probleem met <price_each>.')
        update.message.reply_text(
                '{} <item> <amount> <price_each>'.format(command)
            )
        return DETAIL

    if command == '/sell':
        price = abs(amount * price)
    elif command == '/buy':
        price = -abs(amount * price)

    context.user_data['transaction']['details'].append({
            'item_id': item_id,
            'amount': amount,
            'money': Value(price),
        })

    print_transaction(update, context)

    update.message.reply_text(
            'Voeg meer details toe '
            'of verwijder details met: `/remove <index>`. '
            'Sla de transactie op met: `/save`.',
            parse_mode=ParseMode.MARKDOWN
        )

    return DETAIL


# def conv_transaction_detail_buy(update, context):
#     """Add buy transaction detail"""


# def conv_transaction_detail_add(update, context):
#     """Add transaction detail"""


def conv_transaction_detail_remove(update, context):
    """Remove transaction detail"""
    try:
        index = int(context.args[0]) - 1
    except (IndexError, ValueError):
        update.message.reply_text(
                'geeft detail nummer te verwijderen '
                'met: `/remove <index>`.',
                parse_mode=ParseMode.MARKDOWN
            )
        return DETAIL

    try:
        context.user_data['transaction']['details'].pop(index)
    except IndexError:
        update.message.reply_text(
                'Sorry, die index bestaat niet.'
            )
        return DETAIL

    update.message.reply_text(
            'Transactie detail verwijderd. '
            'Voeg meer details toe '
            'of verwijder details met: `/remove <index>`. '
            'Sla de transactie op met: `/save`.',
            parse_mode=ParseMode.MARKDOWN
        )
    print_transaction(update, context)

    return DETAIL


def conv_transaction_save(update, context):
    """Save transaction"""
    LOGGER.info(
            '%s: CONV add_transaction, CMD save',
            update.message.from_user.username
        )

    if len(context.user_data['transaction']['details']) == 0:
        update.message.reply_text(
                'Oelewapper! '
                'Je hebt geen transactie details toegevoegd.\n' + INSTRUCTIONS,
                parse_mode=ParseMode.MARKDOWN
            )
        return DETAIL

    database.save_transaction(context.user_data['transaction'])

    update.message.reply_text('Transaction opgeslagen')
    context.user_data.clear()

    transaction.cmd_transactions(update, context)

    return ConversationHandler.END


def conv_transaction_cancel(update, context):
    """Cancel transaction"""
    LOGGER.info(
            '%s: CONV add_transaction, CMD cancel',
            update.message.from_user.username
        )
    update.message.reply_text('Transaction gecanceld.')
    context.user_data.clear()

    return ConversationHandler.END


TRANSACTION, DETAIL = range(2)


# add transaction conversation
conversation = ConversationHandler(
        entry_points=[
                CommandHandler(
                        'add_transaction',
                        conv_transaction_start
                    )
            ],
        states={
                TRANSACTION: [
                        MessageHandler(
                                Filters.text,
                                conv_transaction_ask_details
                            )
                    ],
                DETAIL: [
                        CommandHandler(
                                'sell',
                                conv_transaction_detail_add
                            ),
                        CommandHandler(
                                'buy',
                                conv_transaction_detail_add
                            ),
                        CommandHandler(
                                'add',
                                conv_transaction_detail_add
                            ),
                        CommandHandler(
                                'remove',
                                conv_transaction_detail_remove
                            ),
                        CommandHandler(
                                'save',
                                conv_transaction_save
                            ),
                    ]
            },
        fallbacks=[
                CommandHandler(
                        'cancel',
                        conv_transaction_cancel
                    )
            ]
    )
