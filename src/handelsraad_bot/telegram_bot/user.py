"""Telegram user commands"""

# pylint: disable=unused-argument

from telegram import ParseMode

from handelsraad_bot import LOGGER, database, util


def cmd_users(update, context):
    """users command"""
    LOGGER.info('%s: CMD users', update.message.from_user.username)
    if not util.check_permission(update, ['trader', 'chairman'], 'CMD users'):
        return
    users = database.get_users()
    users_msgs = ['*Users:*', '```']
    for user in users:
        users_msgs.append('{:12} {}'.format(
                user.name,
                ', '.join(user.get_roles())
        ))
    if not users:
        users_msgs.append('no users')
    users_msgs.append('```')
    update.message.reply_text(
            '\n'.join(users_msgs), parse_mode=ParseMode.MARKDOWN
        )


def cmd_set_role(update, context):
    """Set role"""
    LOGGER.info('%s: CMD user set role', update.message.from_user.username)
    if not util.check_permission(update, ['chairman'], 'CMD user set role'):
        return
    roles = [
            'chairman',
            'trader',
            'investor',
        ]
    try:
        telegram_username = context.args[0]
        if telegram_username[:1] == '@':
            telegram_username = telegram_username[1:]
    except (IndexError, ValueError):
        LOGGER.warning(
                '%s: CMD user set role, incorrect <username>',
                update.message.from_user.username,
            )
        update.message.reply_text('Probleem met <username>')
        update.message.reply_text('/set_role <username> <role> <boolean>')
        return

    try:
        role = context.args[1]
        if role not in roles:
            raise ValueError
    except (IndexError, ValueError):
        LOGGER.warning(
                '%s: CMD user set role, incorrect <role>',
                update.message.from_user.username,
            )
        update.message.reply_text('Probleem met <role>')
        update.message.reply_text('/set_role <username> <role> <boolean>')
        return

    try:
        boolean = bool(context.args[2].lower() == 'true')
    except (IndexError, ValueError):
        LOGGER.warning(
                '%s: CMD user set role, incorrect <boolean>',
                update.message.from_user.username,
            )
        update.message.reply_text('Probleem met <boolean>')
        update.message.reply_text('/set_role <username> <role> <boolean>')
        return

    database.set_role(telegram_username, role, boolean)

    update.message.reply_text(
            'role set: {} {} {}'.format(telegram_username, role, boolean),
            parse_mode=ParseMode.MARKDOWN
        )
    cmd_users(update, context)
