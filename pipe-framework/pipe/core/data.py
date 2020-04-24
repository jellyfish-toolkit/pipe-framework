import typing as t

from typeguard import typechecked


class StoreException(Exception):
    pass


class PipeException(Exception):
    pass


@typechecked
class Store:
    """Data representation which go through the pipe

    :raises: StoreException
    """
    def __init__(self, data: t.Any = None) -> t.NoReturn:
        self.__data = data

    @property
    def data(self) -> t.Any:
        """ Getter for private __data property, do not allow to use __data directly.
        Allow us to make it immutable. I don't know why at this point.

        :rtype: t.Any
        """
        return self.__data

    @data.setter
    def data(self, data: t.Optional[t.Any] = None) -> t.NoReturn:
        """ I don't know why, but I do not allow mutate object

        :param data: defaults to None
        :type data: t.Any, optional
        :raises: StoreException
        """
        raise StoreException("You can't mutate Store instance")

    def get(self, key: str, default: t.Optional[t.Any] = None) -> t.Any:
        """Getter for data

        :param key:
        :type key: str
        :param default: defaults to None
        :type default: optional
        :return: value from __data object
        :rtype: t.Any
        """
        value = self.data.get(key, default)

        return value

    def extend(self, store):
        data_to_add = store.copy()
        result_data = self.copy()

        result_data.update(data_to_add)

        return self.__class__(data=result_data)

    def copy(self):
        return self.data.copy()
