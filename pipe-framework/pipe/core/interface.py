from pipe.core.data import Store


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
