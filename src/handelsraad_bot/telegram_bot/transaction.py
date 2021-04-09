"""Telegram transactions command"""

#pylint: disable=unused-argument

from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from rival_regions_calc import Value

from handelsraad_bot import LOGGER, ITEMS_INV, database


def cmd_transactions(update, context):
    """transactions command"""
    LOGGER.info('%s: CMD transactions', update.message.chat.username)
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

TRANSACTION, CONFIRM, EDIT = range(3)

def transaction_start(update, context):
    """Start message"""
#    if update.message.chat.id != -293370068:
#        update.message.reply_text(
#                'Geen rechten om transactions te maken.' + \
#                'Contact @bergjnl'
#            )
#        return ConversationHandler.END
    update.message.reply_text('Stuur de beschrijving voor transaction:')
    return TRANSACTION

def transaction_confirm(update, context):
    """Transaction confirm"""
    LOGGER.info('Transaction description: "%s"', update.message.text)
    context.user_data['transaction'] = {
            'description': update.message.text,
            'details': [],
        }
    update.message.reply_text(
        'Verstuur \'confirm\' om te plaatsen, ' + \
            '`/edit <language>` om te bewerken, of /cancel om te stoppen.',
        parse_mode=ParseMode.MARKDOWN
    )
    return CONFIRM

def transaction_detail_remove(update, context):
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

def announcement_update(update, context):
    """Update announcement"""
    updated_text = demoji.replace(update.message.text, '')
    language = context.user_data['edit']
    context.user_data['translations'][language] = updated_text
    return format_announcement(update, context)

def announcement_send(update, context):
    """Send announcement"""
    LOGGER.info('Confirmed announcement:\n%s', context.user_data['announcement'])
    if not TESTING:
        telegram_message = BOT.send_message(
            chat_id=TELEGRAM_ANNOUNCEMENT_CHANNEL,
            text=context.user_data['announcement'],
            parse_mode=ParseMode.MARKDOWN
        )
        BOT.forward_message(
            chat_id=VN_TELEGRAM_CHAT,
            from_chat_id=telegram_message.chat_id,
            message_id=telegram_message.message_id
        )
        webhook = DiscordWebhook(
            url=DISCORD_ANNOUCEMENT_WEBHOOK,
            content=context.user_data['announcement'].replace('*', '**')
        )
        webhook.execute()
        requests.post(
            '{}send_conference_message/{}'.format(PACC_URL, RR_CONFERENCE_ID),
            headers=PACC_HEADERS,
            data={
                'message': context.user_data['conference_announcement']
            }
        )
        requests.post(
            '{}send_conference_notification/{}'.format(PACC_URL, RR_CONFERENCE_ID),
            headers=PACC_HEADERS,
            data={
                'message': context.user_data['conference_announcement']
            }
        )
    update.message.reply_text('Announcement verstuurd')
    context.user_data.clear()
    return ConversationHandler.END

def transaction_cancel(update, context):
    """Cancel transaction"""
    LOGGER.info(
            'Canceled transaction: "%s"',
            context.user_data['transaction']
        )
    update.message.reply_text('Canceled transaction.')
    context.user_data.clear()
    return ConversationHandler.END

# add transaction conversation
conf_add_transaction = ConversationHandler(
        entry_points=[
                CommandHandler(
                        'add_transation',
                        transaction_start
                    )
            ],
        states={
                TRANSACTION: [
                        MessageHandler(
                                Filters.text,
                                transaction_confirm
                            )
                    ],
                CONFIRM: [
                        MessageHandler(
                                'add',
                                transaction_add
                            ),
                        CommandHandler(
                                'edit',
                                transaction_edit
                            ),
                        CommandHandler(
                                'save',
                                transaction_save
                            ),
                        CommandHandler(
                                'cancel',
                                transaction_cancel
                            )
                    ],
                EDIT: [
                        MessageHandler(
                                Filters.text,
                                transaction_update
                            )
                    ]
            },
        fallbacks=[
                CommandHandler(
                        'cancel',
                        transaction_cancel
                    )
            ]
    )
