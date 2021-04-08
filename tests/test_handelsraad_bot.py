"""Handelsraad bot tests"""
# pylint: disable=redefined-outer-name

import pytest

from handelsraad_bot import SESSION
from handelsraad_bot.models import Transaction, TransactionDetail



@pytest.mark.skip()
@pytest.mark.vcr()
def test_add_transaction():
    """Test moels"""
    session = SESSION()
    transaction = Transaction()
    transaction.creator = 'berg_jnl'
    transaction.description = 'Test transaction'
    session.add(transaction)

    transaction_detail = TransactionDetail()
    transaction_detail.item_id = 1011
    transaction_detail.amount = 1e6
    transaction_detail.transaction = transaction
    session.add(transaction_detail)

    session.commit()
    session.close()
