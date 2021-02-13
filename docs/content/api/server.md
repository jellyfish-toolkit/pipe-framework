<a name="pipe.server"></a>
# pipe.server

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/__init__.py#L1)

WSGI App for http related Pipes

<a name="pipe.server.App"></a>
## App Objects

```python
class App()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/__init__.py#L19)

Main WSGI app wrapper which run pipes by request method

<a name="pipe.server.App.route"></a>
#### route

```python
 | route(route: str)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/__init__.py#L34)

Decorator for adding pipe as a handler for a route

**Arguments**:

- `route`: Werkzeug formatted route
:type route: string

<a name="pipe.server.App.wsgi_app"></a>
#### wsgi\_app

```python
 | wsgi_app(environ, start_response)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/__init__.py#L53)

Main WSGI app, see werkzeug documentation for more

<a name="pipe.server.App.run"></a>
#### run

```python
 | run(host: str = '127.0.0.1', port: int = 8000, use_inspection: bool = False, static_folder: t.Optional[str] = None, static_url: str = '/static', *args, **kwargs)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/__init__.py#L81)

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

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/wrappers.py#L1)

<a name="pipe.server.wrappers.make_response"></a>
#### make\_response

```python
make_response(data, is_json: bool = False, *args, **kwargs) -> PipeResponse
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/wrappers.py#L16)

Makes WSGI Response from `data` argument

**Arguments**:

- `is_json`: Flag indicating whether it JSON response, or a plain one
- `data`: Response data

**Returns**:

WSGI Response
:rtype: Response

<a name="pipe.server.http"></a>
# pipe.server.http

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/__init__.py#L2)

<a name="pipe.server.http.transform"></a>
# pipe.server.http.transform

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/transform.py#L1)

<a name="pipe.server.http.transform.TJsonResponseReady"></a>
## TJsonResponseReady Objects

```python
@dataclass
class TJsonResponseReady(Step)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/transform.py#L11)

Converts object from a 'data_field' for a simpliest API representation

<a name="pipe.server.http.exceptions"></a>
# pipe.server.http.exceptions

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/exceptions.py#L1)

<a name="pipe.server.http.load"></a>
# pipe.server.http.load

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/load.py#L1)

<a name="pipe.server.http.load.LJsonResponse"></a>
## LJsonResponse Objects

```python
@dataclass
class LJsonResponse(Step)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/load.py#L11)

Creates JSON response from field in 'data_field' property

<a name="pipe.server.http.load.LResponse"></a>
## LResponse Objects

```python
@dataclass
class LResponse(Step)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/load.py#L26)

Sends plain response from datafield, with status from field status

<a name="pipe.server.http.extract"></a>
# pipe.server.http.extract

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/extract.py#L1)

<a name="pipe.server.http.extract.EFormData"></a>
## EFormData Objects

```python
class EFormData(Step)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/extract.py#L9)

Generic extractor for form data from PipeRequest

<a name="pipe.server.http.extract.EQueryStringData"></a>
## EQueryStringData Objects

```python
class EQueryStringData(Step)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/extract.py#L26)

Generic extractor for data from query string which you can find after ? sign in URL

<a name="pipe.server.http.extract.EJsonBody"></a>
## EJsonBody Objects

```python
class EJsonBody(Step)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/http/extract.py#L40)

Generic extractor for data which came in JSON format

<a name="pipe.server.pipe"></a>
# pipe.server.pipe

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/pipe.py#L1)

<a name="pipe.server.pipe.HTTPPipe"></a>
## HTTPPipe Objects

```python
class HTTPPipe(BasePipe)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/pipe.py#L8)

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

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/pipe.py#L48)

Getter for request object

<a name="pipe.server.pipe.HTTPPipe.run_pipe"></a>
#### run\_pipe

```python
 | run_pipe() -> frozendict
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/server/pipe.py#L57)

The main method.
Takes data and pass through pipe. Handles request and response

:raises: PipeException

