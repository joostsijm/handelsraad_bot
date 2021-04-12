"""Handelsraad bot tests"""
# pylint: disable=redefined-outer-name

import pytest

from handelsraad_bot import SESSION, ITEMS
from handelsraad_bot.models import User, Transaction, TransactionDetail


@pytest.mark.skip()
def test_add_transaction():
    """Test moels"""
    session = SESSION()
    user = session.query(User).filter(User.name == 'Test').first()
    if not user:
        user = User()
        user.name = 'Test'
        user.telegram_id = '1'
        user.telegram_username = 'Test'
        user.trader = True
        session.add(user)

    transaction = Transaction()
    transaction.user = user
    transaction.description = 'Test transaction'
    session.add(transaction)

    transaction_detail = TransactionDetail()
    transaction_detail.money = -18e8
    transaction_detail.item_id = ITEMS['uranium']
    transaction_detail.amount = 1e6
    transaction_detail.transaction = transaction
    session.add(transaction_detail)

    session.commit()
    session.close()
