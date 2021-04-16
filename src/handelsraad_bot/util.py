"""Common utilities"""

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
    resource_details = {}
    for detail in database.get_transaction_details():
        if detail.item_id not in total:
            total[detail.item_id] = {
                    'amount': 0,
                    'average': 0
                }
            resource_details[detail.item_id] = []
        total[detail.item_id]['amount'] += detail.amount
        total[0]['amount'] += detail.money
        resource_details[detail.item_id].append(detail)

    for resource, details in resource_details.items():
        money_total = 0
        resource_total = total[resource]['amount']
        for detail in reversed(details):
            if detail.money > 0:
                continue
            if resource_total < detail.amount:
                money_total += round(
                        resource_total * (detail.money / detail.amount), 2
                    )
                break
            money_total += detail.money
            resource_total -= detail.amount
        total[detail.item_id]['average'] = abs(round(
                money_total / total[resource]['amount'], 2
            ))
    total[0]['amount'] = round(total[0]['amount'] / 1e6) * 1e6
    return total
