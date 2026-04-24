import logging
from unittest.mock import MagicMock

import pytest

from log_exceptions import log_exceptions


# ---------------------------------------------------------------------------
# Helper fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_logger():
    return MagicMock(spec=logging.Logger)


# ---------------------------------------------------------------------------
# Function decorator tests
# ---------------------------------------------------------------------------


class TestFunctionDecorator:
    def test_no_exception_returns_value(self, mock_logger):
        @log_exceptions(mock_logger)
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        mock_logger.exception.assert_not_called()

    def test_exception_is_logged(self, mock_logger):
        @log_exceptions(mock_logger)
        def boom():
            raise ValueError("something went wrong")

        with pytest.raises(ValueError, match="something went wrong"):
            boom()

        mock_logger.exception.assert_called_once_with("something went wrong")

    def test_exception_is_reraised(self, mock_logger):
        @log_exceptions(mock_logger)
        def boom():
            raise RuntimeError("re-raise me")

        with pytest.raises(RuntimeError):
            boom()

    def test_wraps_preserves_metadata(self, mock_logger):
        @log_exceptions(mock_logger)
        def my_func():
            """My docstring."""

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "My docstring."

    def test_logs_error_message_only(self, mock_logger):
        @log_exceptions(mock_logger)
        def boom():
            raise TypeError("type error message")

        with pytest.raises(TypeError):
            boom()

        mock_logger.exception.assert_called_once_with("type error message")


# ---------------------------------------------------------------------------
# Class decorator tests
# ---------------------------------------------------------------------------


class TestClassDecorator:
    def test_methods_wrapped_for_exceptions(self, mock_logger):
        @log_exceptions(mock_logger)
        class MyClass:
            def method_a(self):
                raise ValueError("error in method_a")

            def method_b(self):
                raise RuntimeError("error in method_b")

        obj = MyClass()

        with pytest.raises(ValueError):
            obj.method_a()
        mock_logger.exception.assert_any_call("error in method_a")

        with pytest.raises(RuntimeError):
            obj.method_b()
        mock_logger.exception.assert_any_call("error in method_b")

    def test_methods_returning_values_unaffected(self, mock_logger):
        @log_exceptions(mock_logger)
        class Calculator:
            def multiply(self, a, b):
                return a * b

        calc = Calculator()
        assert calc.multiply(3, 4) == 12
        mock_logger.exception.assert_not_called()

    def test_no_exception_no_log(self, mock_logger):
        @log_exceptions(mock_logger)
        class MyClass:
            def ok(self):
                return "ok"

        obj = MyClass()
        obj.ok()
        mock_logger.exception.assert_not_called()

    def test_class_instance_is_still_usable(self, mock_logger):
        @log_exceptions(mock_logger)
        class Counter:
            def __init__(self):
                self.count = 0

            def increment(self):
                self.count += 1

        c = Counter()
        c.increment()
        c.increment()
        assert c.count == 2
