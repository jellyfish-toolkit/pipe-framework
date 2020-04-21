import copy
import typing as t

from orator import DatabaseManager


class DatabaseBaseMixin:
    """
    Generic mixin for all Steps related to Database
    """
    connection_config: t.Optional[t.Dict[str, str]] = None
    data_field_name: str = 'data'
    pk_field: str = 'id'
    one_shot: bool = True
    table_name: t.Optional[str] = None
    __db = None
    query = None

    def __init__(self, table_name=None, data_field_name='data', pk_field='id', where=(), join=(), one_shot=True):
        self.data_field_name = data_field_name
        self.table_name = table_name
        self.pk_field = pk_field
        self.one_shot = one_shot

    def set_table(self):
        self.query = self.__db.table(self.table_name)
        return self.query

    def set_select(self, to_select: t.Tuple = ()):
        return self.query.select(*to_select)

    def set_where(self, where: t.Tuple = ()):
        return self.query.where(*where)

    def set_join(self, join: t.Tuple = ()):
        if len(join) > 0:
            return self.query.join(*join)

    def create_connection(self) -> t.NoReturn:
        """
        Creates connection to database if it is None
        """
        if self.__db is None:
            self.__db = DatabaseManager(self.connection_config)

    def clear_connection(self):
        """
        Removes connection
        """
        self.__db.disconnect()
        self.__db = None


class CreateUpdateMixin:
    def insert(self, data: t.Dict):
        """
        Inserts data into a table

        :param data:
        :return:
        """
        self.create_connection()
        return self.set_table().insert_get_id(data)

    def update(self, data: t.Dict):
        """
        Updates data in the table

        :param data:
        :return:
        """
        self.create_connection()
        pk = copy.deepcopy(data).pop(self.pk_field)

        self.set_table()
        self.set_where((self.pk_field, '=', pk))

        return self.query.update(data)


class ReadMixin:
    def select(self, to_select: t.Tuple[str] = (), pk: t.Optional[int] = None):
        self.create_connection()
        self.set_table()

        if pk is not None:
            self.set_where((self.pk_field, '=', pk))

        self.set_select(to_select)
        self.set_join()

        if pk is not None:
            return self.query.first()
        else:
            return list(self.query.get())


class DeleteMixin:
    def delete(self, pk: t.Optional[int]):
        self.create_connection()
        self.set_table()
        self.set_where((self.pk_field, '=', pk))

        return self.query.delete()
