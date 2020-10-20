import valideer
from frozendict import frozendict

from pipe.core.base import Loader
from pipe.generics.db.orator_orm.mixins import DatabaseBaseMixin, CreateUpdateMixin, DeleteMixin


class LDBInsertUpdateBase(Loader, DatabaseBaseMixin, CreateUpdateMixin):
    required_fields = {
        '+{table_name}': valideer.Type(str),
        '+{data_field}': valideer.Type(str)
    }

    def load(self, store: frozendict) -> frozendict:
        """
        Loader for inserting or updating database tables

        :param store:
        :return: Store
        """
        # TODO: Something with update or insert checking is wrong, and I didn't figured out why yet
        data_to_load = store.get(self.data_field)
        update = self.pk_field in data_to_load

        if update:
            result = self.update(data_to_load)
        else:
            result = self.insert(data_to_load)

        store = store.copy(**{
            f'{self.table_name}_{"update" if update else "insert"}': result
        })

        return store


class LDatabaseDeleteBase(Loader, DatabaseBaseMixin, DeleteMixin):
    required_fields = {
        '+{table_name}': valideer.Type(str),
        '+{pk_field}': valideer.Type(str)
    }

    def load(self, store: frozendict) -> frozendict:
        pk_to_delete = store.get(self.pk_field)

        self.delete(pk_to_delete)

        return store
