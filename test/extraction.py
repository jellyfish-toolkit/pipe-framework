from pipe.core.base import Extractor
from pipe.core.data import DataObject


class TestExtractor(Extractor):

    def extract(self, data_object: DataObject) -> DataObject:
        data: dict = {
            'some': 'message'
        }

        data.update({
            'request': data_object.data
        })

        return DataObject(data=data)
