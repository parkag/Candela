from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('index_number', Integer),
    Column('nickname', String),
    Column('email', String),
    Column('role', SmallInteger),
    Column('about_me', String),
    Column('last_seen', DateTime),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('password', String(length=200)),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('about_me', String(length=200)),
    Column('last_seen', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['index_number'].drop()
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['index_number'].create()
    post_meta.tables['user'].columns['password'].drop()
