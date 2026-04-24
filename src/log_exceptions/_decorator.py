import functools
import inspect


def log_exceptions(logger):
    """
    Decorator that logs exceptions raised during function or class method
    execution.

    When applied to a function, catches any exception, logs the error message
    using the provided logger, and re-raises the exception.

    When applied to a class, tries to apply the function decorator to the
    methods defined in the class.

    Args:
        logger: A logger object with an ``exception`` method
            (e.g. ``logging.Logger``).

    Returns:
        A decorator that wraps a function or class.
    """

    def decorator(obj):
        if inspect.isclass(obj):
            for name, method in obj.__dict__.items():
                if inspect.isfunction(method):
                    setattr(obj, name, decorator(method))
                elif isinstance(method, staticmethod):
                    setattr(obj, name, staticmethod(decorator(method.__func__)))
                elif isinstance(method, classmethod):
                    setattr(obj, name, classmethod(decorator(method.__func__)))
            return obj

        @functools.wraps(obj)
        def wrapper(*args, **kwargs):
            try:
                return obj(*args, **kwargs)
            except Exception as e:
                logger.exception("%s", e)
                raise

        return wrapper

    return decorator
