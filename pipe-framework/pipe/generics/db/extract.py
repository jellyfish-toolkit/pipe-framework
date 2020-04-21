import copy

from pipe.core.base import Extractor
from pipe.core.data import Store
from pipe.generics.db.utils import DatabaseBaseMixin, ReadMixin


class EDBReadBase(Extractor, DatabaseBaseMixin, ReadMixin):

    def extract(self, store: Store):
        data = store.copy()
        pk = store.get(self.pk_field, False)

        if pk:
            result = self.select(pk=pk)
        else:
            result = self.select()

        if not pk and result is not None:
            data.update({
                f'{self.table_name}_list': [dict(item) for item in result]
            })
        elif pk and result is not None:
            data.update({
                f'{self.table_name}_item': dict(result)
            })

        if self.one_shot:
            self.clear_connection()

        return Store(data)
