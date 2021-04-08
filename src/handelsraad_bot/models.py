"""Models module"""

from datetime import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy_migrate import Migrate


meta = db.MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
})

Base = declarative_base()
#migrate = Migrate()
