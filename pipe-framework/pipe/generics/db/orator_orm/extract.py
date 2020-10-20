import valideer
from frozendict import frozendict

from pipe.core.base import Extractor
from pipe.generics.db.orator_orm.mixins import DatabaseBaseMixin, ReadMixin


class EDBReadBase(Extractor, DatabaseBaseMixin, ReadMixin):

    required_fields = {
        '+{table_name}': valideer.Type(str),
        '+{data_field}': valideer.Type(str)
    }

    def extract(self, store: frozendict):
        pk = store.get(self.pk_field, False)

        if pk:
            result = self.select(pk=pk)
        else:
            result = self.select()

        if not pk and result is not None:
            store = store.copy(**{
                f'{self.table_name}_list': [dict(item) for item in result]
            })
        elif pk and result is not None:
            store = store.copy(**{
                f'{self.table_name}_item': dict(result)
            })

        return store
