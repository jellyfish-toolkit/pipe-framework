from frozendict import frozendict

from pipe.generics.helpers import TLambda, TPutDefaults
from pipe.server import HTTPPipe, app
from pipe.server.http.extract import EFormData
from pipe.server.http.load import LResponse
from src.db.extract import EDatabase
from src.template.transform import TTemplateResponseReady

from src.db.load import LDatabase


@app.route('/')
class FormPage(HTTPPipe):
    pipe_schema = {
        'GET': {
            'out': (
                EDatabase(table_name='todo-items'),
                TLambda(lambda_=lambda store: frozendict(context=dict(
                    items=store.get('todo-items_list')))),
                TTemplateResponseReady(template_name='index.html'),
                LResponse(data_field='template', headers={'Content-Type': 'text/html'})
            ),
        },
        'POST': {
            'in': (
                EFormData(),
                TPutDefaults(defaults={
                    'done': False
                }, field_name='form'),
                LDatabase(data_field='form', table_name='todo-items')
            ),
            'out': (
                EDatabase(table_name='todo-items'),
                TLambda(lambda_=lambda store: frozendict(
                    context=dict(items=store.get('todo-items_list'))
                )),
                TTemplateResponseReady(template_name='index.html'),
                LResponse(data_field='template', headers={'Content-Type': 'text/html'})
            )
        }
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,
            use_debugger=True,
            use_reloader=True,
            use_inspection=True
            )
