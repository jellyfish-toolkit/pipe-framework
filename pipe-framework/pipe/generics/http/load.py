from dataclasses import dataclass

from pipe.core.base import Loader
from pipe.core.data import Store
from pipe.core.utils import make_response


@dataclass
class LJsonResponse(Loader):
    """
    Creates JSON response from field in 'data_field' property
    """
    data_field = 'response'

    def load(self, store: Store):

        self.required_fields = {
            self.data_field: {
                'type': 'object'
            }
        }
        self.validate(store)

        return make_response(Store(store.get(self.data_field)), is_json=True)
