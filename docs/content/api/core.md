<a name="pipe.core.exceptions"></a>
# pipe.core.exceptions

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/exceptions.py#L1)

<a name="pipe.core.base"></a>
# pipe.core.base

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L1)

<a name="pipe.core.base.Step"></a>
## Step Objects

```python
class Step()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L10)

Base class providing basic functionality for all steps related classes

There are three types of steps:

Extractor, Loader, Transformer.

*How to understand which one you need:*

1. If you need to get data (**extract**) from **external** source, you need extractor
2. If you need to send data (**load**) to **external** source, you need loader
3. If you need to interact with data (**transform**) you need transformer

<a name="pipe.core.base.Step.__and__"></a>
#### \_\_and\_\_

```python
 | __and__(other: 'Step') -> 'Step'
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L29)

Overriding boolean AND operation for merging steps:

**Example**:

```python
EUser(pk=1) & EBook(where=('id', 1))
```
  
  In case any of steps throws an exception, nothing happens

<a name="pipe.core.base.Step.__or__"></a>
#### \_\_or\_\_

```python
 | __or__(other: 'Step') -> 'Step'
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L52)

Overriding boolean OR operation for merging steps:

**Example**:

```python
EUser(pk=1) | LError()
```
  
  in case first step throws an exception then store goes to the second step
  with information about an exception in the store
  
  **Arguments**:
  
  - `other`: Step which merge with
  
  **Returns**:
  
  Step which runs both of the steps according to an operator

<a name="pipe.core.base.Step.validate"></a>
#### validate

```python
 | validate(store: frozendict) -> frozendict
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L94)

Validates store according to `Step.required_fields` field

**Arguments**:

- `store`: 

**Returns**:

Store with adapted data

<a name="pipe.core.base.Step.factory"></a>
#### factory

```python
 | @classmethod
 | factory(cls, run_method: t.Callable, name: str = '', **arguments) -> type
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L114)

Step factory, creates step with `run_method` provided

**Arguments**:

- `run_method`: Method which will be runned by pipe
- `name`: Name for a step
- `arguments`: Arguments for a step constructor

**Returns**:

New Step

<a name="pipe.core.base.Step.run"></a>
#### run

```python
 | run(store: frozendict) -> frozendict
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L125)

Method which provide ability to run any step.

Pipe shouldn't know which exactly step is
running, that's why we need run method. But developers should be limited in 3 options,
which presented in `_available_methods`

You can extend this class and change `_available_methods` field, if you want to customize
this behavior

**Arguments**:

- `store`: Current pipe state

**Returns**:

New frozendict object with updated pipe state

<a name="pipe.core.base.BasePipe"></a>
## BasePipe Objects

```python
class BasePipe()
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L150)

Base class for all pipes, implements running logic and inspection of pipe state on every
step

<a name="pipe.core.base.BasePipe.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(initial: t.Mapping, inspection: bool = False)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L159)

**Arguments**:

- `initial`: Initial store state
- `inspection`: Inspection mode on/off

<a name="pipe.core.base.BasePipe.set_inspection"></a>
#### set\_inspection

```python
 | set_inspection(enable: bool = True) -> bool
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L167)

Sets inspection mode

**Examples**:

  
  **Toggle inspection on:**
  
```python
MyPipe({}).set_inspection()
```
  
  **Toggle inspection off:*
  
```python
MyPipe({}).set_inspection(False)
```

<a name="pipe.core.base.BasePipe.before_pipe"></a>
#### before\_pipe

```python
 | before_pipe(store: frozendict) -> frozendict
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L228)

Hook for running custom pipe (or anything) before every pipe execution

**Arguments**:

- `store`: 

**Returns**:

Store

<a name="pipe.core.base.BasePipe.after_pipe"></a>
#### after\_pipe

```python
 | after_pipe(store: frozendict) -> frozendict
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L237)

Hook for running custom pipe (or anything) after every pipe execution

**Arguments**:

- `store`: 

**Returns**:

Store

<a name="pipe.core.base.BasePipe.interrupt"></a>
#### interrupt

```python
 | interrupt(store: frozendict) -> bool
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L246)

Interruption hook which could be overridden, allow all subclassed pipes set one
condition, which will
be respected after any step was run. If method returns true, pipe will not be finished
and will
return value returned by step immediately (respects after_pipe hook)

**Arguments**:

- `store`: 

**Returns**:



<a name="pipe.core.base.NamedPipe"></a>
## NamedPipe Objects

```python
class NamedPipe(BasePipe)
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/base.py#L263)

Simple pipe structure to interact with named pipes.

**Example**:

  
```python
class MyPipe(NamedPipe):
pipe_schema = {
'crop_image': (EImage('<path>'), TCrop(width=230, height=140), LSave('<path>'))
}

image_path = MyPipe(<initial_store>).run_pipe('crop_image')
```

<a name="pipe.core.decorators"></a>
# pipe.core.decorators

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/decorators.py#L1)

<a name="pipe.core.decorators.configure"></a>
#### configure

```python
configure(config: dict) -> t.Callable
```

[[view_source]](https://github.com/jellyfish-tech/pipe-framework/blob/e4b5ede64a00b483b26901ff3d20ee7204baf17f/pipe-framework/pipe/core/decorators.py#L4)

Configures Step class with values from `config variable`
TODO: candidate for deprecation?

**Arguments**:

- `config`: 

**Returns**:



