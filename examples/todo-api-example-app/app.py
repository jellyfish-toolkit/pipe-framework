from pipe.generics.helpers import TLambda
from pipe.server import HTTPPipe, app
from pipe.server.http.extract import EJsonBody
from src.db.load import LDatabase, LDelete
from src.db.extract import EDatabase
from pipe.server.http.load import LJsonResponse, LBadRequest, LNotFound, LResponse
from pipe.server.http.transform import TJsonResponseReady
from src.extract import ETodoJsonBody


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
                TLambda(lambda_=lambda store: store.copy(id=store.get('todo-items_insert'))),
                EDatabase(table_name='todo-items'),
                TJsonResponseReady(data_field='todo-items_item'),
                LJsonResponse()
            )
        }
    }


@app.route('/todo/<int:id>')
class TodoDetailsResource(HTTPPipe):
    pipe_schema = {
        'GET': {
            'out': (
                EDatabase(table_name='todo-items') | LNotFound(),
                TJsonResponseReady(data_field='todo-items_item'),
                LJsonResponse()
            )
        },
        'POST': {
            'in': (
                EJsonBody() | LBadRequest(),
                LDatabase(data_field='json', table_name='todo-items')
            ),
            'out': (
                TJsonResponseReady(data_field='todo-items_insert'), LJsonResponse(status=201)
            )
        },
        'PUT': {
            'in': (
                ETodoJsonBody() | LBadRequest(),
                TLambda(lambda_=lambda store: store.copy(
                    json=dict(**store.get('json'), **{"id": store.get('id')}))),
                LDatabase(data_field='json', table_name='todo-items')
            ),
            'out': (
                EDatabase(table_name='todo-items'),
                TJsonResponseReady(data_field='todo-items_item'), LJsonResponse(status=201)
            )
        },
        'DELETE': {
            'in': (
                LDelete(table_name='todo-items'),
            ),
            'out': (
                LResponse(status=204),
            )
        }
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,
            use_debugger=True,
            use_reloader=True,
            use_inspection=True
            )
