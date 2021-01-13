# Pipe Framework

Data-oriented web microframework allows you to create web services with ETL approach instead of traditional MVC.

**Not related to HBO's Silicon Valley show.**

## Introduction

You won't find Models, Controllers, and Views in the Pipe framework, but I'll use them to demonstrate its principles.

All functionality of the Pipe framework is built using Steps.

Step is a self-sufficient, isolated piece of functionality, which does only one thing at a time
(*single responsibility principle*).


Let me explain this concept in detail.

For example, you have a simple task to create an API endpoint with todo tasks listing.

In the traditional approach, you'll have to create a Todo model, which will represent a database table.
In controller bound to route, you'll use the model instance to **extract** data about todo tasks,
then **transform** it to the http response and send it to the user.

> I've marked **extract** and **transform** so you can link MVC concepts to the concepts used in Pipe framework.

According to the paragraph above, we can set an analogy between **MVC** (Model-View-Controller) and **ETL** (Extract-Transform-Load):

Model -> Extractor

Controller -> Transformer

View -> Loader

This analogy isn't 100% correct but it demonstrates how parts of the approach are related to each other.

> As you can see, I've set the view layer as Loader. I'll explain it a bit later.

## Your first route

Let's implement the above-mentioned task using the Pipe framework.

The first thing you should know is there are three kinds of steps:

* Extractor
* Transformer
* Loader

How to decide which step do you require?

1. If you need to get the data from an external source: extractor.
2. If you need to send data outside of the framework: loader.
3. If you need to change data in some way: transformer.

> That's why View is linked with Loader in the example. You can think of this as of loading data to the user browser.

First, we need to decompose this functionality into smaller parts.
For this task, we need to do the following:

1. Extract data from a database;
2. Transform data to the JSON HTTP response;
3. Load this response to the browser.

So we need 1 extractor, 1 transformer, and 1 loader.
Thankfully, the Pipe framework provides several generic steps, so we can skip some boring parts,
but anyway we need to write our own extractor to set the database access details for the step.

As `Step` is an independent part of the application not aware of anything going beyond the step purpose, it is easily transferable between apps.
The downside of this solution is that we cannot have a centralized configuration repository.
All configuration applying to steps should be stored in the exact step properties, but sometimes it means that
we need to write the same thing every time we write steps sharing the same configuration.

For this purposes, the Pipe framework provides `@configure` decorator. You simply write properties you want to add to the step like here:

```python
DATABASES = {
    'default': {
        'driver': 'postgres',
        'host': 'localhost',
        'database': 'todolist',
        'user': 'user',
        'password': '',
        'prefix': ''
    }
}

DB_STEP_CONFIG = {
    'connection_config': DATABASES
}
```

and then apply this to the step as in the example below:

```python
@configure(DB_STEP_CONFIG)
class EDatabase(EDBReadBase):
    pass
```

> As you can tell, the name of the step begins with a capital letter E.
In the Pipe framework, you always implement Extractors, Transformers and Loaders, but it's really hard to keep names short if you use it like this:
> ```python
> class ExtractTodoFromDatabase(Extractor):
>     pass
> ```
> That is why all generic steps follow an agreement to indicate the step type with the first letter of the step name:
> ```python
> class ETodoFromDatabase(Extractor):
>     pass
> ```
> `E` is for extractor, `T` for transformer and `L` for loader.
> But of course you are free to use any names you want.

So, let's create the project root folder:

`pipe-sample/`

Then create `src` folder inside of the `pipe-sample` folder:

```
pipe-sample/
    src/
```

All database-related steps will be in the db package, so let's create it as well:

```
pipe-sample/
    src/
        db/
            __init__.py
```

Create a `config.py` file, as there will be the database configuration:

`pipe-sample/src/db/config.py`

```python
DATABASES = {
    'default': {
        'driver': 'postgres',
        'host': 'localhost',
        'database': 'todolist',
        'user': 'user',
        'password': '',
        'prefix': ''
    }
}

DB_STEP_CONFIG = {
    'connection_config': DATABASES
}
```
Then create the `extract.py` file to keep our configured extractor:

`pipe-sample/src/db/extract.py`
```python
from src.db.config import DB_STEP_CONFIG # our configuration

"""
Pipe framework includes some generics for database as well,
you can check them in the
API documentation
"""
from pipe.generics.db.orator_orm.extract import EDBReadBase


@configure(DB_STEP_CONFIG) # applying configuration to the step
class EDatabase(EDBReadBase):
    pass
    # we don't need to write anything inside the class,
    # all logic is already implemented inside EDBReadBase
```

> Creating a whole folder structure could be an overhead for one small task, but this was done here to show the preferred folder structure for other projects.

Pretty easy so far. We don't need to repeat these actions with other steps, because they are not
configuration-dependent.

Actually, we're ready to create our first pipe now.

Create `app.py` in the project root. Then put this code to the file:

`pipe-sample/app.py`
```python
from pipe.server import HTTPPipe, app
from src.db.extract import EDatabase
from pipe.server.http.load import LJsonResponse
from pipe.server.http.transform import TJsonResponseReady


@app.route('/todo/') # this decorator tells to the WSGI app that this pipe serves this route
class TodoResource(HTTPPipe):
    """
    we extending HTTPPipe class which provides pipe_schema
    applicable to the http requests
    """

    """
    pipe_schema is a dictionary with sub-pipes for every HTTP method.
    'in' and 'out' is a direction inside the pipe, when pipe handles request,
    first this request goes through 'in' and then through 'out' pipe.
    Here we don't need any processing before the response, so only 'out' is presented
    """
    pipe_schema = {
        'GET': {
            'out': (
                EDatabase(table_name='todo-items'),
                TJsonResponseReady(data_field='todo-items_list'),
                LJsonResponse()
            )
        }
    }


"""
Pipe framework uses Werkzeug as a WSGI server, so configuration is pretty familiar except
'use_inspection' argument. Inspection - is a mode for debugging. In case you set it to True
before step execution framework will print data state and step name to the console
"""
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,
            use_debugger=True,
            use_reloader=True,
            use_inspection=True
            )

```

Now you can execute `$ python app.py` and go to `http://localhost:8000/todo/`.

## Store validation

First, we need to find out what is store in Pipe framework.

### Store

After pipe is started, but before the first step pipe is called `before_pipe` hook (you can use this hook to perform some operations on the store before executing). This hook accepts initial store, created from initial data passed to the pipe.

```python
class BasePipe:
   def __init__(self, initial, inspection: bool = False):
        self.__inspection_mode = inspection
        self.store = self.before_pipe(frozendict(initial))
```

As you can see, store is nothing but the `frozendict` instance. Although you can't manipulate data inside the store, you can still create a new instance using the `frozendict().copy()` method. You can find more information in [readme file](https://github.com/slezica/python-frozendict).

### Validation

Even though steps are independent pieces of functionality, sometimes they could require the specific data in the store to perfom certain operations. For this purposes, there are the `required_fields` field in step configuration.

The Pipe framework uses [Valideer](https://github.com/podio/valideer) for validation, but it's a candidate for the deprecation during the next iterations.

#### Example

All you have to do is to write a dict with the required fields (check [Valideer](https://github.com/podio/valideer) for more information about the available validators).

```python
    required_fields = {'+some_field': valideer.Type(dict)} # `+` means required field
```

#### Dynamic validation

Sometimes, you can have some dynamic fields in step, showing which store field contains required information.
You can't know how this field is named, but you do know in what step variable this value is available.
If you want to validate these fields as well, you'll have to add curly braces, inside which the name of a class field will be.

```python
    required_fields = {'+{pk_field}': valideer.Type(dict)} # everything else is the same
```
The Pipe framework will substitute class field value for this field automatically, and then perform validation.

## Steps arithmetics

You can combine two or more steps in case you need some conditional execution.

In this example, you can see the first operation available - `|` (OR)

```python
    pipe_schema = {
        'GET': {
            'out': (
                # In this case, if EDatabase step throws
                # any exception, then LNotFound step will be executed, with information about exception
                # in store
                EDatabase(table_name='todo-items') | LNotFound(),
                TJsonResponseReady(data_field='todo-items_item'),
                LJsonResponse()
            )
        },
```

There is also the second operator - `&` (AND)

```python
    pipe_schema = {
        'GET': {
            'out': (
                # In this case, if EDatabase step throws
                # any exception, or SomethingImportantAsWell throws any exception
                # then nothing happens and store without a change goes to next step
                EDatabase(table_name='todo-items') & SomethingImportantAsWell(),
                TJsonResponseReady(data_field='todo-items_item'),
                LJsonResponse()
            )
        },
```
