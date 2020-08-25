import os

from src.db.load import LDatabase
from pipe.generics.http.extract import EJsonBody
from src.db.extract import EDatabase
from pipe.core import app
from pipe.core.base import HTTPPipe
from pipe.generics.http.load import LJsonResponse
from pipe.generics.http.transform import TJsonResponseReady


@app.route('/todo/')
class TodoResource(HTTPPipe):
    pipe_schema = {
        'GET': {
            'out': (
                EDatabase(
                    table_name='todo-items',
                ),
                TJsonResponseReady(
                    data_field='todo-items_list'
                ),
                LJsonResponse()
            )
        },
        'POST': {
            'in': (
                EJsonBody(),
                LDatabase(
                    data_field='json',
                    table_name='todo-items'
                )
            ),
            'out': (
                TJsonResponseReady(
                    data_field='todo-items_insert'
                ),
                LJsonResponse()
            )
        }
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,
            use_debugger=True,
            use_reloader=True,
            use_inspection=True,
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
            )
