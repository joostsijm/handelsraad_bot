"""Telegram transactions command"""

# pylint: disable=unused-argument

from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, \
        ConversationHandler

from rival_regions_calc import Value

from handelsraad_bot import LOGGER, ITEMS, ITEMS_INV


def print_transaction(update, context):
    """Print transaction"""
    index = 1
    total_money = 0
    transaction_msg = [
            'Transaction omschrijving: "{}"'.format(
                    context.user_data['transaction']['description']
                ),
            'Details:',
            ]
    for detail in context.user_data['transaction']['details']:
        transaction_msg.append(
                '*{}*: {}, {}, $ {}'.format(
                        index,
                        detail['amount'],
                        ITEMS_INV[detail['item_id']],
                        detail['money']
                    )
            )
        index += 1
        total_money += detail['money']

    transaction_msg.append('Totaal geld: $ {}'.format(Value(total_money)))

    update.message.reply_text(
            '\n'.join(transaction_msg),
            parse_mode=ParseMode.MARKDOWN
        )


def conv_transaction_start(update, context):
    """Start message"""
    LOGGER.info('%s: CMD add_transaction', update.message.chat.username)
#    if update.message.chat.id != -293370068:
#        update.message.reply_text(
#                'Geen rechten om transactions te maken.' + \
#                'Contact @bergjnl'
#            )
#        return ConversationHandler.END
    update.message.reply_text('Stuur de beschrijving voor transactie:')
    return TRANSACTION


def conv_transaction_ask_details(update, context):
    """Transaction ask details"""
    LOGGER.info(
            '%s: CMD add_transaction, description: "%s"',
            update.message.chat.username,
            update.message.text
        )
    context.user_data['transaction'] = {
            'description': update.message.text,
            'details': [],
        }
    update.message.reply_text(
            """Voeg transactie details toe.
```
/sell <item> <amount> <price_each>
/buy <item> <amount> <price_each>
/add <item> <amount> <money>
```
bijvoorbeeld:
```
/sell uranium 1kk 2000
/add uranium 1kk 2kkk
/buy oil 10kkk 190
/add oil 10kkk -1900kkk```""",
            parse_mode=ParseMode.MARKDOWN
        )
    return CONFIRM


def conv_transaction_sell(update, context):
    """Add sell transaction detail"""
    try:
        item_id = ITEMS[context.args[0]]
    except (IndexError, KeyError):
        LOGGER.info(
                '%s: CMD transaction sell, incorrect item name',
                update.message.chat.username,
            )
        update.message.reply_text('Probleem met item <name>.')
        update.message.reply_text('/sell <item> <amount> <price_each>')
        return CONFIRM

    try:
        amount = Value(context.args[1])
    except (IndexError, ValueError):
        LOGGER.info(
                '%s: CMD transaction sell, incorrect amount',
                update.message.chat.username,
            )
        update.message.reply_text('Probleem met <amount>.')
        update.message.reply_text('/sell <item> <amount> <price_each>')
        return CONFIRM

    try:
        price_each = Value(context.args[2])
    except (IndexError, ValueError):
        LOGGER.info(
                '%s: CMD transaction sell, incorrect price each',
                update.message.chat.username,
            )
        update.message.reply_text('Probleem met <price_each>.')
        update.message.reply_text('/sell <item> <amount> <price_each>')
        return CONFIRM

    context.user_data['transaction']['details'].append({
            'item_id': item_id,
            'amount': amount,
            'money': Value(amount * price_each),
        })

    print_transaction(update, context)

    update.message.reply_text(
            'Voeg meer details toe of sla de transactie op met `/save`.',
            parse_mode=ParseMode.MARKDOWN
        )

    return CONFIRM


def conv_transaction_buy(update, context):
    """Add buy transaction detail"""


def conv_transaction_add(update, context):
    """Add add transaction detail"""


def conv_transaction_detail_remove(update, context):
    """Edit language text"""
    try:
        index = int(context.args[0]) - 1
    except IndexError:
        update.message.reply_text(
                'geeft detail detail nummer te verwijderen.'
            )
    context.user_data['transaction']['details'].pop(index)

    update.message.reply_text('Transaction detail verwijderd')
    return EDIT


def conv_transaction_save(update, context):
    """Save transaction"""
    LOGGER.info(
            '%s: CMD save transaction',
            update.message.chat.username
        )
    update.message.reply_text('Transaction opgeslagen')
    context.user_data.clear()
    return ConversationHandler.END


def conv_transaction_cancel(update, context):
    """Cancel transaction"""
    LOGGER.info(
            '%s: CMD cancel transaction',
            update.message.chat.username
        )
    update.message.reply_text('Transaction gecanceld.')
    context.user_data.clear()
    return ConversationHandler.END


TRANSACTION, CONFIRM, EDIT = range(3)


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
                CONFIRM: [
                        CommandHandler(
                                'sell',
                                conv_transaction_sell
                            ),
                        CommandHandler(
                                'buy',
                                conv_transaction_buy
                            ),
                        CommandHandler(
                                'add',
                                conv_transaction_add
                            ),
#                        CommandHandler(
#                                'edit',
#                                conv_transaction_edit
#                            ),
#                        CommandHandler(
#                                'save',
#                                conv_transaction_save
#                            ),
                    ],
                EDIT: [
#                        MessageHandler(
#                                Filters.text,
#                                conv_transaction_update
#                            )
                    ]
            },
        fallbacks=[
                CommandHandler(
                        'cancel',
                        conv_transaction_cancel
                    )
            ]
    )
