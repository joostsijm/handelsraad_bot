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
