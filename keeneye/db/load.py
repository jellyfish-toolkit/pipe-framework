import typing as t

from sqlalchemy import create_engine, MetaData, Table, Column, String

from pipe.core.data import Store
from pipe.core.base import Loader
from sqlalchemy.engine.url import URL


class LDBLoaderBase(Loader):
    connection_string: t.Optional[str] = None
    connection_conf: dict = {}
    meta = MetaData(engine)
    some_table = Table(
        'user', meta,
        Column('data', String),
    )
    meta.create_all(engine)

    def __init__(self, connection_string, connection_conf, store_class=Store):
        self.connection_string = connection_string
        self.connection_conf = connection_conf
        self.__store_class = store_class

    def sqlalchemy_conn_db(self):
        if connection_string is not None:
            url = URL(**connection_string)
        else:
            url = URL(**connection_conf)
        engine = create_engine(url, echo=True)
        connection = engine.connect()
        return connection

    def insert_data(self, connection, some_table):
        insert_statement = some_table.insert().values(self.store_class)
        connection.execute(insert_statement)

    def update_data(self, connection, some_table):
        update_statement = some_table.update().where(some_table.c.data).values(self.store_class)
        connection.execute(update_statement)


class LDBLoaderPostgres(LDBLoaderBase):
    connection_string: str = 'postgresql://username:qwerty1@127.0.0.1:8000/mydb'
    # connection_conf = dict(
    #     drivername='postgresql',
    #     username='username',
    #     password='qwerty1',
    #     host='127.0.0.1',
    #     port='8000',
    #     database='mydb',
    # )

# class LUserWithReallyHardToUnderstandRelations(LDBLoaderPostgres):
#
#   def load(self, store: Store):




