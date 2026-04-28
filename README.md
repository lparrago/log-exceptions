# log-exceptions

A Python decorator that automatically catches, logs, and re-raises exceptions — ensuring exceptions are recorded in your log files and not only printed to the screen.

## Installation

```bash
pip install log-exceptions
```

## Usage

The `log_exceptions` decorator takes a logger object (any object with an `exception` method, such as `logging.Logger`) and wraps the decorated function or class so that any exception is logged before being re-raised.

### Decorate a function

```python
import logging
from log_exceptions import log_exceptions

logger = logging.getLogger(__name__)

@log_exceptions(logger)
def divide(a, b):
    return a / b

divide(1, 0)  # ZeroDivisionError is logged and re-raised
```

### Decorate a class

Applying the decorator to a class wraps **all** instance methods defined on that class.

```python
import logging
from log_exceptions import log_exceptions

logger = logging.getLogger(__name__)

@log_exceptions(logger)
class Calculator:
    def divide(self, a, b):
        return a / b

    def multiply(self, a, b):
        return a * b

calc = Calculator()
calc.divide(1, 0)  # ZeroDivisionError is logged and re-raised
```

### Decorate a class with a `staticmethod`

Static methods are detected and wrapped automatically.

```python
import logging
from log_exceptions import log_exceptions

logger = logging.getLogger(__name__)

@log_exceptions(logger)
class MathUtils:
    @staticmethod
    def divide(a, b):
        return a / b

MathUtils.divide(1, 0)  # ZeroDivisionError is logged and re-raised
```

### Decorate a class with a `classmethod`

Class methods are detected and wrapped automatically.

```python
import logging
from log_exceptions import log_exceptions

logger = logging.getLogger(__name__)

@log_exceptions(logger)
class MathUtils:
    @classmethod
    def divide(cls, a, b):
        return a / b

MathUtils.divide(1, 0)  # ZeroDivisionError is logged and re-raised
```
