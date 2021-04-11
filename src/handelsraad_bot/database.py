"""Database"""

# pylint: disable=singleton-comparison

from datetime import datetime

from sqlalchemy.orm import joinedload

from handelsraad_bot import SESSION
from handelsraad_bot.models import User, Transaction, TransactionDetail, Limit


def get_total():
    """Get total"""
    session = SESSION()
    total = {
            0: 0,
        }
    for user in session.query(User).filter(User.investment != None).all():
        total[0] += user.investment
    transaction_details = session.query(TransactionDetail).all()
    for detail in transaction_details:
        if detail.item_id not in total:
            total[detail.item_id] = 0
        total[detail.item_id] += detail.amount
        total[0] += detail.money
    session.close()
    return total


def get_limits():
    """Get limits"""
    session = SESSION()
    limits = {}
    for limit in session.query(Limit).all():
        limits[limit.item_id] = limit.amount
    session.close()
    return limits


def set_limit(item_id, amount):
    """Set limit"""
    session = SESSION()
    limit = session.query(Limit).filter(Limit.item_id == item_id).first()
    if not limit:
        limit = Limit()
        limit.item_id = item_id
        session.add(limit)
    limit.amount = amount
    session.commit()
    session.close()


def remove_limit(item_id):
    """Remove limit"""
    session = SESSION()
    limit = session.query(Limit).filter(Limit.item_id == item_id).first()
    if limit:
        session.delete(limit)
        session.commit()


def get_transactions(limit=5):
    """Get transactions"""
    session = SESSION()
    transactions = session.query(Transaction).options(
            joinedload('details')
        ).limit(limit).all()
    session.close()
    return transactions


def save_transaction(transaction_dict):
    """Save transaction"""
    session = SESSION()
    user = session.query(User).filter(
            User.telegram_id == transaction_dict['telegram_id']
        ).first()
    if not user:
        user = User()
        user.name = 'test'
        user.telegram_id = transaction_dict['telegram_id']
        user.trader = True
        session.add(user)

    transaction = Transaction()
    transaction.date_time = datetime.now()
    transaction.description = transaction_dict['description']
    transaction.user = user
    session.add(transaction)

    for detail in transaction_dict['details']:
        transaction_detail = TransactionDetail()
        transaction_detail.money = detail['money']
        transaction_detail.item_id = detail['item_id']
        transaction_detail.amount = detail['amount']
        transaction_detail.transaction = transaction
        session.add(transaction_detail)

    session.commit()
    session.close()
