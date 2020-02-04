import typing as t


class DataObjectException(Exception):
    pass


class PipeException(Exception):
    pass


class DataObject():
    """Data representation which go through the pipe

    :raises: DataObjectException
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
        :raises: DataObjectException
        """
        raise DataObjectException("You can't mutate DataObject instance")
