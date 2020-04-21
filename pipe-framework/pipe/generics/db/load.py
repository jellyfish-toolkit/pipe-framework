import copy
import typing as t

from pipe.core.base import Loader
from pipe.core.data import Store
from pipe.generics.db.utils import DatabaseBaseMixin, CreateUpdateMixin, DeleteMixin


class LDBInsertUpdateBase(Loader, DatabaseBaseMixin, CreateUpdateMixin):

    def __init__(self, hard_update: bool = False, *args, **kwargs):
        self.hard_update = hard_update

        super().__init__(*args, **kwargs)

    def load(self, store: Store) -> Store:
        """
        Loader for inserting or updating database tables

        :param store:
        :return: Store
        """
        data = store.copy()

        data_to_load = data.get(self.data_field_name)
        update = self.pk_field in data_to_load

        if update:
            result = self.update(data_to_load)
        else:
            result = self.insert(data_to_load)

        if self.one_shot:
            self.clear_connection()

        data.update({
            f'{self.table_name}_{"update" if update else "insert"}': result
        })

        return Store(data)


class LDatabaseDeleteBase(Loader, DatabaseBaseMixin, DeleteMixin):

    def load(self, store: Store) -> Store:
        data = store.copy()
        pk_to_delete = data.get(self.pk_field)

        self.delete(pk_to_delete)

        if self.one_shot:
            self.clear_connection()

        return Store(data)
