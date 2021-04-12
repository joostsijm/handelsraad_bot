"""Database models"""

# pylint: disable=too-few-public-methods

from datetime import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


meta = db.MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
})

Base = declarative_base()


class User(Base):
    """Moel for user"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    telegram_id = db.Column(db.Integer, nullable=False)
    chairman = db.Column(db.Boolean, default=False, nullable=False)
    trader = db.Column(db.Boolean, default=False, nullable=False)
    investor = db.Column(db.Boolean, default=False, nullable=False)


class Investment(Base):
    """Model for investment"""
    __tablename__ = 'investment'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship(
        'User', backref=backref('investments', lazy='dynamic')
    )


class Transaction(Base):
    """Model for deal"""
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship(
        'User', backref=backref('transactions', lazy='dynamic')
    )


class TransactionDetail(Base):
    """Model for transaction detail"""
    __tablename__ = 'transaction_detail'
    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.BigInteger, nullable=False)
    item_id = db.Column(db.SmallInteger, nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
    transaction_id = db.Column(
                db.Integer, db.ForeignKey('transaction.id'), nullable=False
            )
    transaction = relationship(
        'Transaction', backref=backref('details')
    )


class Limit(Base):
    """Model for limit"""
    __tablename__ = 'limit'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.SmallInteger, nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)


class Profit(Base):
    """Model for profit"""
    __tablename__ = 'profit'
    id = db.Column(db.Integer, primary_key=True)
    profit_type = db.Column(db.SmallInteger, nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
    transaction_id = db.Column(
            db.Integer, db.ForeignKey('transaction.id'), nullable=False
        )
    transaction = relationship(
        'Transaction', backref=backref('profits', lazy='dynamic')
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = relationship(
        'User', backref=backref('profits', lazy='dynamic')
    )
