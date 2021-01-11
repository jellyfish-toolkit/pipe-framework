---
menu: main
title: Generics
---

<a name="pipe.generics.template"></a>
# pipe.generics.template

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/template/__init__.py#L2)

<a name="pipe.generics.template.transform"></a>
# pipe.generics.template.transform

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/template/transform.py#L1)

<a name="pipe.generics.template.transform.TJinja2TemplateResponseReady"></a>
## TJinja2TemplateResponseReady Objects

```python
class TJinja2TemplateResponseReady(Transformer)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/template/transform.py#L10)

<a name="pipe.generics.template.transform.TJinja2TemplateResponseReady.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(template_name='', **options)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/template/transform.py#L17)

Setting Jinja2 environment
you can provide any options you can find in Jinja2 documentation.
By default we setting only loader and autoescape, but you can rewrite it too.

<a name="pipe.generics.db"></a>
# pipe.generics.db

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/__init__.py#L2)

<a name="pipe.generics.db.orator_orm"></a>
# pipe.generics.db.orator\_orm

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/__init__.py#L2)

<a name="pipe.generics.db.orator_orm.mixins"></a>
# pipe.generics.db.orator\_orm.mixins

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L1)

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin"></a>
## DatabaseBaseMixin Objects

```python
class DatabaseBaseMixin()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L9)

Generic mixin for all Steps related to Database

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_table"></a>
#### set\_table

```python
 | set_table(table_name: str)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L41)

**Arguments**:

- `table_name`: 

**Returns**:

Orator Query builder

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_select"></a>
#### set\_select

```python
 | set_select(select: t.Optional[tuple] = None)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L50)

Sets columns for selecting. See Orator docs for detailed info

**Arguments**:

- `select`: 

**Returns**:



<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.set_where"></a>
#### set\_where

```python
 | set_where(where: t.Optional[tuple] = None)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L59)

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

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L69)

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

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L79)

Creates connection to database if it is None

<a name="pipe.generics.db.orator_orm.mixins.DatabaseBaseMixin.clear_connection"></a>
#### clear\_connection

```python
 | clear_connection()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L86)

Clears connection

<a name="pipe.generics.db.orator_orm.mixins.CreateUpdateMixin"></a>
## CreateUpdateMixin Objects

```python
class CreateUpdateMixin()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L94)

<a name="pipe.generics.db.orator_orm.mixins.CreateUpdateMixin.insert"></a>
#### insert

```python
 | insert(data: t.Dict)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L95)

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

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L105)

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

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L126)

Small mixin which implements simplest 'select' operation for extracting.
If this method does not fulfill all your requirements, you have to create your own extractor.

<a name="pipe.generics.db.orator_orm.mixins.ReadMixin.select"></a>
#### select

```python
 | select(pk: t.Optional[int] = None) -> t.Union[t.Mapping, list]
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L131)

Returns list of the objects from database or just one object, if 'pk' param is presented

**Arguments**:

- `pk`: 

<a name="pipe.generics.db.orator_orm.mixins.DeleteMixin"></a>
## DeleteMixin Objects

```python
class DeleteMixin()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L153)

<a name="pipe.generics.db.orator_orm.mixins.DeleteMixin.delete"></a>
#### delete

```python
 | delete(pk: t.Optional[int] = None)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/mixins.py#L154)

Deletes object by a 'pk' or by a where clause if presented

**Arguments**:

- `pk`: 

<a name="pipe.generics.db.orator_orm.load"></a>
# pipe.generics.db.orator\_orm.load

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/load.py#L1)

<a name="pipe.generics.db.orator_orm.load.LDBInsertUpdateBase"></a>
## LDBInsertUpdateBase Objects

```python
class LDBInsertUpdateBase(Loader,  DatabaseBaseMixin,  CreateUpdateMixin)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/load.py#L10)

<a name="pipe.generics.db.orator_orm.load.LDBInsertUpdateBase.load"></a>
#### load

```python
 | load(store: frozendict) -> frozendict
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/load.py#L13)

Loader for inserting or updating database tables

**Arguments**:

- `store`: 

**Returns**:

Store

<a name="pipe.generics.db.orator_orm.extract"></a>
# pipe.generics.db.orator\_orm.extract

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/extract.py#L1)

<a name="pipe.generics.db.orator_orm.extract.EDBReadBase"></a>
## EDBReadBase Objects

```python
class EDBReadBase(Extractor,  DatabaseBaseMixin,  ReadMixin)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/orator_orm/extract.py#L8)

Base step for extracting data from database. Requires configuration for connecting to the database

**Example**:

  
  >>>   @configure(DB_STEP_CONFIG)
  >>>   class EDatabase(EDBReadBase):
  >>>      pass
  
  Usage example:
  
  >>> EDatabase(table_name='todo-items'),

<a name="pipe.generics.db.exceptions"></a>
# pipe.generics.db.exceptions

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/db/exceptions.py#L1)

<a name="pipe.generics.helpers"></a>
# pipe.generics.helpers

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/helpers.py#L1)

<a name="pipe.generics.helpers.TPutDefaults"></a>
## TPutDefaults Objects

```python
@dataclass
class TPutDefaults(Transformer)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/c7c2af29dec158d024950b69bc7e2bdd2310bd84/pipe-framework/pipe/generics/helpers.py#L10)

Helper transformers, which puts values from defaults into Store

