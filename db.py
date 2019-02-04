import asyncpgsa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime
)
from sqlalchemy.sql import select

metadata = MetaData()


clients = Table(
    'clients', metadata,
    Column('id', String(36), primary_key=True),
    Column('url', String(1024), nullable=False),
    Column('email', String(120)),
    Column('status', String(8), nullable=False),
    Column('md5_hash', String(120))
)


async def create_table(conn):
    await conn.execute('DROP TABLE IF EXISTS clients')
    await conn.execute('''CREATE TABLE clients (
    id varchar(36) PRIMARY KEY,
    url varchar(1024) NOT NULL,
    email varchar(120),
    status varchar(8) NOT NULL,
    md5_hash varchar(120))''')


async def init_db(app):
    dsn = construct_db_url(app['config']['database'])
    pool = await asyncpgsa.create_pool(dsn=dsn)
    app['db_pool'] = pool
    async with app['db_pool'].acquire() as conn:
        await create_table(conn)


def construct_db_url(config):
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )


async def get_data_by_id(conn, uid):
    result = await conn.fetchrow(
        clients
        .select()
        .where(clients.c.id == uid)
    )
    return result


async def create_request(conn, uid, url, email=None,
                         status='running', md5_hash=None):
    await conn.execute(
        clients
        .insert()
        .values(id=uid, url=url, email=email, status=status, md5_hash=md5_hash)
    )


async def insert_hash(conn, uid, status='failed', md5_hash=None):
    await conn.execute(
        clients
        .update()
        .values(status=status, md5_hash=md5_hash)
        .where(clients.c.id == uid)
    )
