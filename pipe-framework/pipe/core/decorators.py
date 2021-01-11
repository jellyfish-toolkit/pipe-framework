def configure(config):
    """
    Configures Step class with values from `config variable`
    :param config:
    :return:
    """
    def decorator(wrapped):
        for key, value in config.items():
            setattr(wrapped, key, value)

        return wrapped

    return decorator
