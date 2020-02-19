import typing as t


class StoreException(Exception):
    pass


class PipeException(Exception):
    pass


class Store():
    """Data representation which go through the pipe

    :raises: StoreException
    """
    def __init__(self, data: t.Any = None):
        self.__data = data

    @property
    def data(self) -> t.Any:
        """ Getter for private __data property, do not allow to use __data directly.
        Allow us to make it immutable. I don't know why at this point.

        :rtype: t.Any
        """
        return self.__data

    @data.setter
    def data(self, data: t.Any = None):
        """ I don't know why, but I do not allow mutate object

        :param data: defaults to None
        :type data: t.Any, optional
        :raises: StoreException
        """
        raise StoreException("You can't mutate Store instance")

    def get(self, key: str, default: t.Optional[str] = None):
        """Getter for data

        :param key:
        :type key: str
        :param default: defaults to None
        :type default: optional
        :return: value from __data object
        :rtype: t.Any
        """
        value = self.__data.get(key, default)

        return value
