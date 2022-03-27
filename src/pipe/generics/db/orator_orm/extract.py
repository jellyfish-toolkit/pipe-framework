from frozendict import frozendict
from pipe.core.base import Step
from pipe.generics.db.exceptions import DatabaseException
from pipe.generics.db.orator_orm.mixins import DatabaseBaseMixin, ReadMixin


class EDBReadBase(Step, DatabaseBaseMixin, ReadMixin):
    """
    Base step for extracting data from database. Requires configuration for connecting to the
    database

    Example:

    ```python
    @configure(DB_STEP_CONFIG)
    class EDatabase(EDBReadBase):
       pass
    ```

    Usage example:

    ```python
    EDatabase(table_name='todo-items', where=('id', 1), join=('table_name', 'id', '<', 'some_id'))
    ```

    """
    def extract(self, store: frozendict) -> frozendict:
        pk = store.get(self.pk_field, False)

        result = self.select(pk=pk) if pk else self.select()

        if not pk and result is not None:
            store = store.copy(**{f'{self.table_name}_list': [dict(item) for item in result]})
        elif result is not None:
            store = store.copy(**{f'{self.table_name}_item': dict(result)})
        else:
            raise DatabaseException(f'Result for table {self.table_name} is empty')

        return store
