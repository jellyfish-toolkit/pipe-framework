def configure(config):
    def decorator(wrapped):
        for key, value in config.items():
            setattr(wrapped, key, value)

        return wrapped

    return decorator
