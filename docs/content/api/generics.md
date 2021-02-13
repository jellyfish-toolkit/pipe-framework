<a name="pipe.generics.template"></a>
# pipe.generics.template

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/template/__init__.py#L2)

<a name="pipe.generics.template.transform"></a>
# pipe.generics.template.transform

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/template/transform.py#L1)

<a name="pipe.generics.template.transform.TTemplateResponseReady"></a>
## TTemplateResponseReady Objects

```python
class TTemplateResponseReady(Step)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/template/transform.py#L9)

<a name="pipe.generics.template.transform.TTemplateResponseReady.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(template_name='', **options)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/template/transform.py#L16)

Setting Jinja2 environment
you can provide any options you can find in Jinja2 documentation.
By default we setting only loader and autoescape, but you can rewrite it too.

<a name="pipe.generics.db"></a>
# pipe.generics.db

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/__init__.py#L2)

<a name="pipe.generics.db.orator_orm"></a>
# pipe.generics.db.orator\_orm

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/__init__.py#L2)

<a name="pipe.generics.db.orator_orm.mixins"></a>
# pipe.generics.db.orator\_orm.mixins

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L1)

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin"></a>
## DatabaseBaseMixin Objects

```python
class DatabaseBaseMixin()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L9)

Generic mixin for all Steps related to Database

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_table"></a>
#### set\_table

```python
 | set_table(table_name: str) -> QueryBuilder
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L41)

**Arguments**:

- `table_name`: 

**Returns**:

Orator Query builder

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_select"></a>
#### set\_select

```python
 | set_select(select: t.Optional[tuple] = None) -> QueryBuilder
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L50)

Sets columns for selecting. See Orator docs for detailed info

**Arguments**:

- `select`: 

**Returns**:

Orator Query builder

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_where"></a>
#### set\_where

```python
 | set_where(where: t.Optional[tuple] = None) -> QueryBuilder
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L59)

Sets where clause. See Orator docs for detailed info

**Arguments**:

- `where`: 

**Returns**:

Orator Query builder

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_join"></a>
#### set\_join

```python
 | set_join(_join: t.Optional[tuple] = None) -> QueryBuilder
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L69)

Sets join clause. See Orator docs for detailed info.

**Arguments**:

- `_join`: 

**Returns**:

Orator Query builder

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.create_connection"></a>
#### create\_connection

```python
 | create_connection() -> None
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L79)

Creates connection to database if it is None

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.clear_connection"></a>
#### clear\_connection

```python
 | clear_connection()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L86)

Clears connection

<a name="pipe.generics.db.orator_orm.mixins.CreateUpdateMixin"></a>
## CreateUpdateMixin Objects

```python
class CreateUpdateMixin()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L93)

<a name="pipe.generics.db.orator_orm.mixins.CreateUpdateMixin.insert"></a>
#### insert

```python
 | insert(data: t.Dict) -> int
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L94)

Inserts data into a table

**Arguments**:

- `data`: 

**Returns**:

id of inserted string

<a name="pipe.generics.db.orator_orm.mixins.CreateUpdateMixin.update"></a>
#### update

```python
 | update(data: t.Dict) -> int
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L104)

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

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L125)

Small mixin which implements simplest 'select' operation for extracting.
If this method does not fulfill all your requirements, you have to create your own extractor.

<a name="pipe.generics.db.orator_orm.mixins.ReadMixin.select"></a>
#### select

```python
 | select(pk: t.Optional[int] = None) -> t.Union[t.Mapping, list]
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L130)

Returns list of the objects from database or just one object, if 'pk' param is presented

**Arguments**:

- `pk`: 

<a name="pipe.generics.db.orator_orm.mixins.DeleteMixin"></a>
## DeleteMixin Objects

```python
class DeleteMixin()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L152)

<a name="pipe.generics.db.orator_orm.mixins.DeleteMixin.delete"></a>
#### delete

```python
 | delete(pk: t.Optional[int] = None) -> int
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L153)

Deletes object by a 'pk' or by a where clause if presented

**Arguments**:

- `pk`: 

<a name="pipe.generics.db.orator_orm.load"></a>
# pipe.generics.db.orator\_orm.load

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/load.py#L1)

<a name="pipe.generics.db.orator_orm.load.LDBInsertUpdateBase"></a>
## LDBInsertUpdateBase Objects

```python
class LDBInsertUpdateBase(Step,  DatabaseBaseMixin,  CreateUpdateMixin)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/load.py#L7)

Loader for inserting or updating into database tables

**Example**:

  
```python
LDatabase(data_field='json', table_name='todo-items')
```

<a name="pipe.generics.db.orator_orm.load.LDatabaseDeleteBase"></a>
## LDatabaseDeleteBase Objects

```python
class LDatabaseDeleteBase(Step,  DatabaseBaseMixin,  DeleteMixin)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/load.py#L30)

Loader for deleting from database tables

**Example**:

  
```python
LDatabase(table_name='todo-items')
```

<a name="pipe.generics.db.orator_orm.extract"></a>
# pipe.generics.db.orator\_orm.extract

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/extract.py#L1)

<a name="pipe.generics.db.orator_orm.extract.EDBReadBase"></a>
## EDBReadBase Objects

```python
class EDBReadBase(Step,  DatabaseBaseMixin,  ReadMixin)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/orator_orm/extract.py#L7)

Base step for extracting data from database. Requires configuration for connecting to the
database

**Example**:

  
```python
@configure(DB_STEP_CONFIG)
class EDatabase(EDBReadBase):
pass
```
  
  Usage example:
  
```python
EDatabase(table_name='todo-items', where=('id', 1), join=('table_name', 'id', '<', 'some_id'))
```

<a name="pipe.generics.db.exceptions"></a>
# pipe.generics.db.exceptions

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/db/exceptions.py#L1)

<a name="pipe.generics.helpers"></a>
# pipe.generics.helpers

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/helpers.py#L1)

<a name="pipe.generics.helpers.TPutDefaults"></a>
## TPutDefaults Objects

```python
@dataclass
class TPutDefaults(Step)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/helpers.py#L9)

Helper transformers, which puts values from `defaults` into `Store`, to specific `field_name`

<a name="pipe.generics.helpers.TLambda"></a>
## TLambda Objects

```python
@dataclass
class TLambda(Step)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/acb48de510fe270ff4255c65c9c5b351a448e71c/pipe-framework/pipe/generics/helpers.py#L21)

Step for small transformations of a store. Useful for cases where writing specific step is an overengineering

