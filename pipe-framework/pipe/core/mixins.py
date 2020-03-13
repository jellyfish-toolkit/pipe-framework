import typing as t

from pipe.core.data import Store
from schema import Schema


class RunnableException(Exception):
    pass


class RunnableMixin:
    """Interface for every pipe element.
    Loader, Transformer and Extractor should implement
    run method to easily go through pipe.

    """

    def run(self, store: Store):
        """Method to implement. Takes data object, cause directly participate in
        piping process

        :param store:
        :type data: Store
        """
        pass

class ValidatableMixin:
    required_fields: dict = {}
    errors: t.Optional[list] = None
    validated_data: t.Any = None
    save_validated: bool = True

    def validate(self, store: Store, ignore_extra_keys: bool = True):
        current_schema = Schema(self.required_fields, ignore_extra_keys=ignore_extra_keys)

        result = current_schema.validate(store.data)

        if self.save_validated:
            self.validated_data = Store(data=result)

        return result
