from pipe.core.base import Transformer
from pipe.core.data import DataObject


class TestTransformer(Transformer):

    def transform(self, data_object: DataObject) -> DataObject:

        data = data_object.data

        data.update({
            'one': 'more'
        })

        return DataObject(data)
