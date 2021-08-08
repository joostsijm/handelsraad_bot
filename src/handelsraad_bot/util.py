"""Common utilities"""

from rival_regions_calc import Value

from handelsraad_bot import LOGGER, TESTING, database


def check_permission(update, roles, action):
    """Check permissions"""
    executor = database.get_user_by_telegram_id(
            update.message.from_user.id
        )
    if not executor:
        executor = database.get_user_by_telegram_username(
                update.message.from_user.username
            )
        if executor:
            executor.telegram_id = update.message.from_user.id
            executor = database.save_user(executor)
        else:
            executor = database.add_user(
                    update.message.from_user.first_name,
                    update.message.from_user.id,
                    update.message.from_user.username
                )
    if TESTING:
        return True
    for role in executor.get_roles():
        if role in roles:
            return True
    LOGGER.warning(
            '%s: %s, not allowed',
            update.message.from_user.username,
            action
        )
    update.message.reply_text(
            'Rollen die recht hebben op dit command: {}'.format(
                    ', '.join(roles)
                )
        )
    return False


def total_investment(user):
    """Count user investment"""
    total = 0
    for investment in user.investments:
        total += investment.amount
    return total


def get_total():
    """Get total including average"""
    total = {
            0: {
                    'amount': 0,
                    'average': 0
                }
        }
    for user in database.get_investors():
        total[0]['amount'] += total_investment(user)
    item_details = {}
    for detail in database.get_transaction_details():
        if detail.item_id not in total:
            total[detail.item_id] = {
                    'amount': 0,
                    'average': 0
                }
            item_details[detail.item_id] = []
        total[detail.item_id]['amount'] += detail.amount
        total[0]['amount'] += detail.money
        item_details[detail.item_id].append(detail)

    for item_id, details in item_details.items():
        money_total = 0
        item_total = total[item_id]['amount']
        for detail in reversed(details):
            if detail.money >= 0:
                continue
            if item_total < detail.amount:
                money_total += round(
                        item_total * (detail.money / detail.amount), 2
                    )
                break
            money_total += detail.money
            item_total -= detail.amount
        if total[item_id]['amount']:
            total[detail.item_id]['average'] = abs(round(
                    money_total / total[item_id]['amount'], 2
                ))
        else:
            del total[item_id]

    return total

def round_number(number, length):
    """Round number"""
    i = 1
    number = Value(number)
    while len(str(number)) > length:
        amount = pow(1000, i)
        number =  Value(round(number / amount) * amount)
        i += 1
    return number
