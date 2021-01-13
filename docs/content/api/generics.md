<a name="pipe.generics.template"></a>
# pipe.generics.template

<a name="pipe.generics.template.transform"></a>
# pipe.generics.template.transform

<a name="pipe.generics.template.transform.TJinja2TemplateResponseReady"></a>
## TJinja2TemplateResponseReady Objects

```python
class TJinja2TemplateResponseReady(Transformer)
```

<a name="pipe.generics.template.transform.TJinja2TemplateResponseReady.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(template_name='', **options)
```

Setting Jinja2 environment
you can provide any options you can find in Jinja2 documentation.
By default we setting only loader and autoescape, but you can rewrite it too.

<a name="pipe.generics.db"></a>
# pipe.generics.db

<a name="pipe.generics.db.orator_orm"></a>
# pipe.generics.db.orator\_orm

<a name="pipe.generics.db.orator_orm.mixins"></a>
# pipe.generics.db.orator\_orm.mixins

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin"></a>
## DatabaseBaseMixin Objects

```python
class DatabaseBaseMixin()
```

Generic mixin for all Steps related to Database

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_table"></a>
#### set\_table

```python
 | set_table(table_name: str)
```

**Arguments**:

- `table_name`: 

**Returns**:

Orator Query builder

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_select"></a>
#### set\_select

```python
 | set_select(select: t.Optional[tuple] = None)
```

Sets columns for selecting. See Orator docs for detailed info

**Arguments**:

- `select`: 

**Returns**:



<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_where"></a>
#### set\_where

```python
 | set_where(where: t.Optional[tuple] = None)
```

Sets where clause. See Orator docs for detailed info

**Arguments**:

- `where`: 

**Returns**:

Orator Query builder

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_join"></a>
#### set\_join

```python
 | set_join(_join: t.Optional[tuple] = None)
```

Sets join clause. See Orator docs for detailed info.

**Arguments**:

- `_join`: 

**Returns**:

Orator Query builder

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.create_connection"></a>
#### create\_connection

```python
 | create_connection() -> t.NoReturn
```

Creates connection to database if it is None

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.clear_connection"></a>
#### clear\_connection

```python
 | clear_connection()
```

Clears connection

<a name="pipe.generics.db.orator_orm.mixins.CreateUpdateMixin"></a>
## CreateUpdateMixin Objects

```python
class CreateUpdateMixin()
```

<a name="pipe.generics.db.orator_orm.mixins.CreateUpdateMixin.insert"></a>
#### insert

```python
 | insert(data: t.Dict)
```

Inserts data into a table

**Arguments**:

- `data`: 

**Returns**:

id of inserted string

<a name="pipe.generics.db.orator_orm.mixins.CreateUpdateMixin.update"></a>
#### update

```python
 | update(data: t.Dict)
```

Updates data in the table

**Arguments**:

- `data`: 

**Returns**:

query instance

<a name="pipe.generics.db.orator_orm.mixins.ReadMixin"></a>
## ReadMixin Objects

```python
class ReadMixin()
```

Small mixin which implements simplest 'select' operation for extracting.
If this method does not fulfill all your requirements, you have to create your own extractor.

<a name="pipe.generics.db.orator_orm.mixins.ReadMixin.select"></a>
#### select

```python
 | select(pk: t.Optional[int] = None) -> t.Union[t.Mapping, list]
```

Returns list of the objects from database or just one object, if 'pk' param is presented

**Arguments**:

- `pk`: 

<a name="pipe.generics.db.orator_orm.mixins.DeleteMixin"></a>
## DeleteMixin Objects

```python
class DeleteMixin()
```

<a name="pipe.generics.db.orator_orm.mixins.DeleteMixin.delete"></a>
#### delete

```python
 | delete(pk: t.Optional[int] = None)
```

Deletes object by a 'pk' or by a where clause if presented

**Arguments**:

- `pk`: 

<a name="pipe.generics.db.orator_orm.load"></a>
# pipe.generics.db.orator\_orm.load

<a name="pipe.generics.db.orator_orm.load.LDBInsertUpdateBase"></a>
## LDBInsertUpdateBase Objects

```python
class LDBInsertUpdateBase(Loader,  DatabaseBaseMixin,  CreateUpdateMixin)
```

<a name="pipe.generics.db.orator_orm.load.LDBInsertUpdateBase.load"></a>
#### load

```python
 | load(store: frozendict) -> frozendict
```

Loader for inserting or updating database tables

**Arguments**:

- `store`: 

**Returns**:

Store

<a name="pipe.generics.db.orator_orm.extract"></a>
# pipe.generics.db.orator\_orm.extract

<a name="pipe.generics.db.orator_orm.extract.EDBReadBase"></a>
## EDBReadBase Objects

```python
class EDBReadBase(Extractor,  DatabaseBaseMixin,  ReadMixin)
```

Base step for extracting data from database. Requires configuration for connecting to the
database

**Example**:

  
  >>>   @configure(DB_STEP_CONFIG)
  >>>   class EDatabase(EDBReadBase):
  >>>      pass
  
  Usage example:
  
  >>> EDatabase(table_name='todo-items'),

<a name="pipe.generics.db.exceptions"></a>
# pipe.generics.db.exceptions

<a name="pipe.generics.helpers"></a>
# pipe.generics.helpers

<a name="pipe.generics.helpers.TPutDefaults"></a>
## TPutDefaults Objects

```python
@dataclass
class TPutDefaults(Transformer)
```

Helper transformers, which puts values from defaults into Store

