from pipe.core import app
from pipe.core.base import Pipe

from test.extraction import TestExtractor
from test.transformer import TestTransformer
from test.loader import TestLoader


@app.path('/')
class HelloWorldPipe(Pipe):

    response_pipe = [
        TestExtractor(), TestTransformer(), TestLoader()
    ]


if __name__ == '__main__':
    app.run(use_reloader=True, use_debugger=True)
