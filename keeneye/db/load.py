import typing as t

from sqlalchemy import create_engine, MetaData, Table, Column, String

from pipe.core.data import Store
from pipe.core.base import Loader
from sqlalchemy.engine.url import URL


class LDBLoaderBase(Loader):
    connection_string: t.Optional[str] = None
    connection_conf: dict = {}

    def __init__(self, data_field: t.Optional[str] = None, table_name: t.Optional[str] = None):
        self.table_name = table_name
        self.data_field = data_field

    def get_db_conn(self):
        if self.connection_string:
            url = self.connection_string
        else:
            url = URL(**self.connection_conf)
        engine = create_engine(url, echo=True)
        connection = engine.connect()
        return connection

    def get_data(self, store: Store):
        data = store.get(self.data_field)
        return data

    def insert_data(self, data):
        insert_statement = self.table_name.insert().values(data)
        self.get_db_conn().execute(insert_statement)

    def update_data(self, data):
        update_statement = self.table_name.update().values(data)
        self.get_db_conn().execute(update_statement)





