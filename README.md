# Pipe Framework

Data oriented web microframework.
Allows you to create web-services with ETL approach instead of traditional MVC.

**Not related to the HBO's Silicon Valley show.**

![Lint](https://github.com/jellyfish-tech/pipe-framework/workflows/Lint/badge.svg?branch=master)

## Introduction

In Pipe framework you'll not find Models, Controllers and Views, but I will use them to demonstrate 
Pipe framework principles

All functionality in Pipe framework built with Steps. 

Step is self-sufficient, isolated piece of functionality, which do only one thing at a time 
(*single responsibility principle*)


Let me explain this concept in detail.

For example you have simple task - create API endpoint with todo tasks listing.

In traditional approach you'll have to create a Todo model which will represent table in database.
In controller bound to route you'll use model instance to **extract** data about todo tasks,
then you'll **transform** it to the http response and send to the user. 

> I marked **extract** and **transform** so you can link MVC concepts to the concepts used in Pipe framework.

According to the paragraph above we can set an analogy between **MVC** (Model-View-Controller) and **ETL** (Extract-Transform-Load)

Model -> Extractor

Controller -> Transformer

View -> Loader

This analogy isn't 100% correct, but demonstrates how parts of the approach is related to each other. 

> As you can see I set view layer as Loader. I'll explain it a bit later   

## Your first route

Let's implement task above with Pipe framework. 

First thing you should know is that there are three kind of steps:

* Extractor
* Transformer
* Loader

How to decide which exact step you require:

1. If you need to get the data from external source - you need extractor.
2. If you need to send data outside of the framework - you need loader
3. If you need to change data in some way - you need transformer. 
 
> That is why View in example above linked with Loader. You can think about this as loading data to the user browser.

As first we need to decompose this functionality to smaller parts. 
For this task we need to do next things. 

1. Extract data from database
2. Transform data to the JSON HTTP response
3. Load this response to the browser

So we need 1 extractor, 1 transformer and 1 loader. 
Thankfully, Pipe framework provides several generic steps so we can skip some boring parts, 
but anyway we need to write our own extractor because we need to set database access details for the step.

In Pipe framework `Step` is an independent part of the application not aware of anything not related to the step purpose.
Thereby every step is easy transferable between apps.
The downside of this solution is that we cannot have a centralized configuration repository.
All configuration applying to steps should be stored in exact step properties, but sometimes it means that 
we need to write the same thing every time we write steps sharing same configuration. 

For this purposes Pipe framework provides `@configure` decorator. You simply write properties you want to add to the step like here:

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

and then apply this to the step as in example below.

```python
@configure(DB_STEP_CONFIG)
class EDatabase(EDBReadBase):
    pass
```

> As you can see in the name of the step we have capital E at the first place.
In Pipe framework you always implement Extractors, Transformers and Loaders, but it's really hard to keep names short if you use it like this:
> ```python
> class ExtractTodoFromDatabase(Extractor):
>     pass
> ```
> that is why all generic steps follow an agreement to indicate type of the step with first letter of the step name:
> ```python
> class ETodoFromDatabase(Extractor):
>     pass
> ```
> `E` is for extractor, `T` for transformer and `L` for loader.
> But of course you are free to use any names you want.

So, let's create project root folder

`pipe-sample/`

then create `src` folder inside `pipe-sample` folder

```
pipe-sample/
    src/
```

all database related steps will be in the db package, so let's create it as well.

``` 
pipe-sample/
    src/
        db/
            __init__.py
```

create a `config.py` file, there will be configuration for the database

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
then create `extract.py` file to keep our configured extractor

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

> Creating a whole folder structure could be an overhead for one small task, but this was done here to show preferred folder structure for another projects

Pretty easy so far. We don't need to repeat this actions with another steps, because they are not 
configuration-dependent.  

Actually now we ready to create our first pipe.

Create an `app.py` in project root. Then put this code to the file:

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

As first we need to find out what is store in Pipe Framework

### Store 

When pipe started, before the first step pipe calls `before_pipe` hook 
(you can use this hook to perform some operations on the store before executing)

```python        
class BasePipe:
   def __init__(self, initial, inspection: bool = False):
        self.__inspection_mode = inspection
        self.store = self.before_pipe(frozendict(initial))
```

as you can see above, store is nothing but `frozendict` instance. You can't manipulate data inside the store,
but you can create new instance with `frozendict().copy()` method. You can find more in corresponding 
[readme file](https://github.com/slezica/python-frozendict)

### Validation

Steps are independent unaware pieces of functionality, but sometimes for perfoming some operations
step could require some specific data in the store. For this purposes there are `required_fields` field
in step configuration. 

Pipe Framework uses [Valideer](https://github.com/podio/valideer) for validation, but it is a candidate for 
deprecation in next iterations

#### Example

All you have to do is write a dict with required fields (check [Valideer](https://github.com/podio/valideer) 
for more information about available validators)

```python
    required_fields = {'+some_field': valideer.Type(dict)} # `+` means required field
```

#### Dynamic validation

Sometimes in step you can have some dynamic fields, showing which store field contains required information.
You can't know how this field named, but you know in what step variable this value is available. 
If you want to validate this fields as well you have to add curly braces inside which there will be name of class field

```python
    required_fields = {'+{pk_field}': valideer.Type(dict)} # everything else is the same                             
```                                                                                    
Pipe framework will substitute this field with class field value automatically, and then perform validation. 

## Steps arithmetics

You can combine two or more steps in case you need some conditional execution. 

In this example you can see first available operation - `|` (OR)

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

There is also second operator - `&` (AND)

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
