"""Database"""

from handelsraad_bot import SESSION
from handelsraad_bot.models import TransactionDetail, Limit


def get_totals():
    """Get totals"""
    session = SESSION()
    totals = {}
    transaction_details = session.query(TransactionDetail).all()
    for detail in transaction_details:
        if detail.item_id not in totals:
            totals[detail.item_id] = 0
        totals[detail.item_id] += detail.amount
    return totals

def get_limits():
    """Get limits"""
    session = SESSION()
    limits = {}
    for limit in session.query(Limit).all():
        limits[limit.item_id] = limit.amount
    return limits

def set_limit(item_id, amount):
    """Set limit"""
    session = SESSION()
    limit = session.query(Limit) \
            .filter(Limit.item_id == item_id).first()
    if not limit:
        limit = Limit()
        limit.item_id = item_id
        session.add(limit)
    limit.amount = amount
    session.commit()

def remove_limit(item_id):
    """Remove limit"""
    session = SESSION()
    limit = session.query(Limit) \
            .filter(Limit.item_id == item_id).first()
    if limit:
        session.delete(limit)
        session.commit()
