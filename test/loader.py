from pipe.core.base import Loader
from pipe.core.data import DataObject
from pipe.core.utils import make_response


class TestLoader(Loader):

    def load(self, data_object: DataObject):

        response = make_response(data_object, status=200)

        return response
