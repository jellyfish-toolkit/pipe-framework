import os
import typing as t

from pipe.core.base import Extractor
from pipe.core.data import Store


class StaticExtractorBase(Extractor):

    static_dir: t.Optional[str] = None
    accepted_formats: t.List[str] = ['text/css', 'image/jpeg', 'image/gif', 'image/png', 'image/svg']

    required_fields = {'file_name': str}

    def extract(self, store: Store):

        file_name = self.validated_data.get('file_name')
        path = os.path.join(self.static_dir, file_name)

        with open(path, 'r') as f:
            content = f.read()

        new_store = store.data

        new_store.update({file_name: content})

        return Store(data=new_store)
