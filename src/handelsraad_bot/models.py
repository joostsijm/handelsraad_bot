"""Database models"""

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


class Transaction(Base):
    """Model for deal"""
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.String, nullable=False)
    creator = db.Column(db.String, nullable=False)


class TransactionDetail(Base):
    """Model for transaction detail"""
    __tablename__ = 'transaction_detail'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.SmallInteger, nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)

    transaction = relationship(
        'Transaction', backref=backref('transaction_details', lazy='dynamic')
    )


class Limit(Base):
    """Model for limit"""
    __tablename__ = 'limit'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.SmallInteger, nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
