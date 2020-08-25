import re
import types

from valideer import accepts


def configure(config):
    def decorator(wrapped):
        def wrapper(*args, **kwargs):
            for key, value in config.items():
                setattr(wrapped, key, value)

            return wrapped(*args, **kwargs)

        return wrapper
    return decorator


def validate(validation_config):
    def decorator(wrapped):
        def wrapper(*args, **kwargs):
            step = wrapped(*args, **kwargs)
            dynamic_config = {}

            for key in validation_config.keys():
                if (key.startswith('+{') or key.startswith('{')) and key.endswith('}'):
                    variable_name = re.match(r'^+?{([a-z_A-Z])+\}$', key).pop()
                    dynamic_config.update({
                        getattr(step, variable_name): validation_config.get(key)
                    })
                    del validation_config[key]

            merged_config = dict(**validation_config, **dynamic_config)

            step.required_fields = merged_config
            step.run_method = step.run

            @accepts(store=validation_config)
            def validate_before_run(self, store):
                return self.run_method(store)

            step.run = types.MethodType(validate_before_run, step)

            return step

        return wrapper
    return decorator
