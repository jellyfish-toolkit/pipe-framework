import copy
import typing as t

from orator import DatabaseManager

from pipe.core.exceptions import StepInitializationException


class DatabaseBaseMixin:
    """
    Generic mixin for all Steps related to Database
    """
    connection_config: t.Dict[str, str]
    __db = None
    query = None
    data_field = None
    table_name = None
    pk_field = None

    def __init__(
        self,
        table_name: t.Optional[str] = None,
        data_field: t.Optional[str] = None,
        pk_field: str = 'id',
        where: t.Optional[tuple] = None,
        join: t.Optional[tuple] = None,
        select: t.Optional[tuple] = None
    ):

        self.data_field = data_field if data_field is not None else self.data_field
        self.table_name = table_name if table_name is not None else self.table_name
        self.pk_field = pk_field if pk_field is not None else self.pk_field

        if self.table_name is None:
            raise StepInitializationException('`table_name` is missing')

        self.where_clause = where
        self.join_clause = join
        self.select_clause = select

    def set_table(self, table_name: str):
        """
        :param table_name:
        :return: Orator Query builder
        """
        self.query = self.__db.table(table_name)

        return self.query

    def set_select(self, select: t.Optional[tuple] = None):
        """
        Sets columns for selecting. See Orator docs for detailed info
        :param select:
        :return:
        """
        if select is not None:
            return self.query.select(*select)

    def set_where(self, where: t.Optional[tuple] = None):
        """
        Sets where clause. See Orator docs for detailed info

        :param where:
        :return: Orator Query builder
        """
        if where is not None:
            return self.query.where(*where)

    def set_join(self, _join: t.Optional[tuple] = None):
        """
        Sets join clause. See Orator docs for detailed info.

        :param _join:
        :return: Orator Query builder
        """
        if _join is not None:
            return self.query.join(*_join)

    def create_connection(self) -> t.NoReturn:
        """
        Creates connection to database if it is None
        """
        if self.__db is None:
            self.__db = DatabaseManager(self.connection_config)

    def clear_connection(self):
        """
        Clears connection
        """
        self.__db.disconnect()
        self.__db = None


class CreateUpdateMixin:
    def insert(self, data: t.Dict):
        """
        Inserts data into a table

        :param data:
        :return: id of inserted string
        """
        self.create_connection()
        return self.set_table(self.table_name).insert_get_id(data)

    def update(self, data: t.Dict):
        """
        Updates data in the table

        :param data:
        :return: query instance
        """
        self.create_connection()
        pk = copy.deepcopy(data).pop(self.pk_field)

        self.set_table(self.table_name)

        if pk is not None:
            self.set_where((self.pk_field, '=', pk, 'and'))

        self.set_where(self.where_clause)
        self.set_join(self.join_clause)

        return self.query.update(data)


class ReadMixin:
    """
    Small mixin which implements simplest 'select' operation for extracting.
    If this method does not fulfill all your requirements, you have to create your own extractor.
    """
    def select(self, pk: t.Optional[int] = None) -> t.Union[t.Mapping, list]:
        """
        Returns list of the objects from database or just one object, if 'pk' param is presented

        :param pk:
        """
        self.create_connection()
        self.set_table(self.table_name)
        self.set_select(self.select_clause)

        if pk is not None:
            self.set_where((self.pk_field, '=', pk, 'and'))

        self.set_where(self.where_clause)
        self.set_join(self.join_clause)

        if pk is not None:
            return self.query.first()
        else:
            return list(self.query.get())


class DeleteMixin:
    def delete(self, pk: t.Optional[int] = None):
        """
        Deletes object by a 'pk' or by a where clause if presented

        :param pk:
        """
        self.create_connection()

        self.set_table(self.table_name)

        if self.where_clause is not None:
            self.set_where(self.where_clause)
        else:
            self.set_where((self.pk_field, '=', pk, 'and'))

        self.set_join(self.join_clause)

        return self.query.delete()
