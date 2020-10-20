from pipe.server import HTTPPipe, app
from pipe.server.http.extract import EJsonBody
from src.db.load import LDatabase
from src.db.extract import EDatabase, ETodoById
from pipe.server.http.load import LJsonResponse, l_bad_request, LNotFound
from pipe.server.http.transform import TJsonResponseReady


@app.route('/todo/')
class TodoResource(HTTPPipe):
    pipe_schema = {
        'GET': {
            'out': (
                EDatabase(table_name='todo-items'),
                TJsonResponseReady(data_field='todo-items_list'),
                LJsonResponse()
            )
        },
        'POST': {
            'in': (
                EJsonBody(), LDatabase(data_field='json', table_name='todo-items')
            ),
            'out': (
                TJsonResponseReady(data_field='todo-items_insert'), LJsonResponse()
            )
        }
    }


@app.route('/todo/<int:id>')
class TodoDetailsResource(HTTPPipe):
    pipe_schema = {
        'GET': {
            'out': (
                ETodoById(table_name='todo-items') | l_bad_request(),
                TJsonResponseReady(data_field='todo-items_item') | LNotFound(),
                LJsonResponse()
            )
        },
        'PUT': {
            'in': (EJsonBody(), LDatabase(data_field='json', table_name='todo-items'))
        },
        'PATCH': {
            'in': (EJsonBody(), LDatabase(data_field='json', table_name='todo-items'))
        }
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,
            use_debugger=True,
            use_reloader=True,
            use_inspection=True
            )
