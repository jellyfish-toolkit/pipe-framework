<a name="pipe.server"></a>
# pipe.server

WSGI App for http related Pipes

<a name="pipe.server.App"></a>
## App Objects

```python
class App()
```

Main WSGI app wrapper which run pipes by request method

<a name="pipe.server.App.route"></a>
#### route

```python
 | route(route: str)
```

Decorator for adding pipe as a handler for a route

**Arguments**:

- `route`: Werkzeug formatted route
:type route: string

<a name="pipe.server.App.wsgi_app"></a>
#### wsgi\_app

```python
 | wsgi_app(environ, start_response)
```

Main WSGI app, see werkzeug documentation for more

<a name="pipe.server.App.run"></a>
#### run

```python
 | run(host: str = '127.0.0.1', port: int = 8000, use_inspection: bool = False, static_folder: t.Optional[str] = None, static_url: str = '/static', *args, **kwargs)
```

Method for running application, actually pretty similar to the Flask run method

**Arguments**:

- `host`: which host use for serving, defaults to '127.0.0.1'
:type host: str, optional

- `port`: which port to listen, defaults to 8000
:type port: int, optional

- `static_folder`: points to the folder with the static files, for serving
:type static_folder: str, optional

- `static_url`: on what endpoint app should serve static files
:type static_url: str

- `use_inspection`: Toggle on inspection mode of the framework
:type use_inspection: bool

<a name="pipe.server.wrappers"></a>
# pipe.server.wrappers

<a name="pipe.server.wrappers.make_response"></a>
#### make\_response

```python
make_response(data, is_json: bool = False, *args, **kwargs) -> PipeResponse
```

Makes WSGI Response from `data` argument

**Arguments**:

- `is_json`: Flag indicating whether it JSON response, or a plain one
- `data`: Response data

**Returns**:

WSGI Response
:rtype: Response

<a name="pipe.server.http"></a>
# pipe.server.http

<a name="pipe.server.http.transform"></a>
# pipe.server.http.transform

<a name="pipe.server.http.transform.TJsonResponseReady"></a>
## TJsonResponseReady Objects

```python
@dataclass
class TJsonResponseReady(Step)
```

Converts object from a 'data_field' for a simpliest API representation

<a name="pipe.server.http.exceptions"></a>
# pipe.server.http.exceptions

<a name="pipe.server.http.load"></a>
# pipe.server.http.load

<a name="pipe.server.http.load.LJsonResponse"></a>
## LJsonResponse Objects

```python
@dataclass
class LJsonResponse(Step)
```

Creates JSON response from field in 'data_field' property

<a name="pipe.server.http.load.LResponse"></a>
## LResponse Objects

```python
@dataclass
class LResponse(Step)
```

Sends plain response from datafield, with status from field status

<a name="pipe.server.http.extract"></a>
# pipe.server.http.extract

<a name="pipe.server.http.extract.EFormData"></a>
## EFormData Objects

```python
class EFormData(Step)
```

Generic extractor for form data from PipeRequest

<a name="pipe.server.http.extract.EQueryStringData"></a>
## EQueryStringData Objects

```python
class EQueryStringData(Step)
```

Generic extractor for data from query string which you can find after ? sign in URL

<a name="pipe.server.http.extract.EJsonBody"></a>
## EJsonBody Objects

```python
class EJsonBody(Step)
```

Generic extractor for data which came in JSON format

<a name="pipe.server.pipe"></a>
# pipe.server.pipe

<a name="pipe.server.pipe.HTTPPipe"></a>
## HTTPPipe Objects

```python
class HTTPPipe(BasePipe)
```

Pipe structure for the `server` package.

Pipe structure. Contains two parts - pipe for request and pipe for response.
Data goes in next way
(in): request extractor -> request transformer -> request loader
(out): response extractor -> response transformer -> response loader

**Example**:

  
```python
@app.route('/todo/')
class TodoResource(HTTPPipe):
pipe_schema = {
'GET': {
'out': (
EDatabase(table_name='todo-items'), TJsonResponseReady(data_field='todo-items_list'), LJsonResponse()
)
},
'POST': {
'in': (EJsonBody(), LDatabase(data_field='json', table_name='todo-items')),
'out': (
TLambda(lambda_=lambda store: store.copy(id=store.get('todo-items_insert'))),
EDatabase(table_name='todo-items'), TJsonResponseReady(data_field='todo-items_item'), LJsonResponse()
)
}
}
```

<a name="pipe.server.pipe.HTTPPipe.request"></a>
#### request

```python
 | @property
 | request() -> PipeRequest
```

Getter for request object

<a name="pipe.server.pipe.HTTPPipe.run_pipe"></a>
#### run\_pipe

```python
 | run_pipe() -> frozendict
```

The main method.
Takes data and pass through pipe. Handles request and response

:raises: PipeException

