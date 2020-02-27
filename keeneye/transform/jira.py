from pipe.core.base import Transformer
from pipe.core.data import Store


class PutDefaultsTransformer(Transformer):

    required_fields = {
        'form': dict
    }

    defaults = {
        'base_url': 'https://jellyfishtech.atlassian.net',
        'email': 'rlatyshenko.dev@gmail.com',
        'api_key': 'Pc4YdcblApRoUPJOp6366310'
    }

    def transform(self, store: Store) -> Store:

        form = store.data.get('form')
        form.update(self.defaults)

        return Store(data=form)

