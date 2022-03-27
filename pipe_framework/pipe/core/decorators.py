import typing as t


def configure(config: dict) -> t.Callable:
    """Configures Step class with values from `config variable` TODO: candidate
    for deprecation?
    """

    def decorator(wrapped: t.Callable) -> t.Callable:
        for key, value in config.items():
            setattr(wrapped, key, value)

        return wrapped

    return decorator
