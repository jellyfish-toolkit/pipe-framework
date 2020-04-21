from abc import ABC, abstractmethod
import typing as t

from pipe.core.data import Store
from cerberus import Validator, TypeDefinition


class RunnableException(Exception):
    pass


class Runnable(ABC):
    """Interface for every pipe element.
    Loader, Transformer and Extractor should implement
    run method to easily go through pipe.

    """

    @abstractmethod
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

    def set_custom_types(self) -> Validator:
        object_type = TypeDefinition('object', (object,), ())
        Validator.types_mapping['object'] = object_type

        return Validator

    def validate(self, store: Store, allow_uknown: bool = True):

        v = self.set_custom_types()(allow_uknown=allow_uknown, require_all=True)
        result = v.validate(store.data, self.required_fields)

        if self.save_validated:
            self.validated_data = Store(data=v.normalized(store.data, self.required_fields))

        return result
