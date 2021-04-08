"""Database models"""

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
    date_time = db.Column(db.DateTime)
    description = db.Column(db.String)
    creator = db.Column(db.String)


class TransactionDetail(Base):
    """Model for transaction detail"""
    __tablename__ = 'transaction_detail'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.SmallInteger)
    amount = db.Column(db.BigInteger)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    transaction = relationship(
        'Transaction', backref=backref('transaction_details', lazy='dynamic')
    )


class Limit(Base):
    """Model for limit"""
    __tablename__ = 'transaction_detail'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.SmallInteger)
    amount = db.Column(db.BigInteger)
