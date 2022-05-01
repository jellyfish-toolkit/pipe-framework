from core.base import SimplePipe
from core.tests.conftest import TestState


def test_simple(pipe_instance: SimplePipe[TestState], expected_result):
    result = pipe_instance()

    assert result == expected_result
