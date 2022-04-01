from typing import List, TypedDict

import pytest
from core.base import SimplePipe

from pipe_framework.core.factories import create_simple_pipe


class TestState(TypedDict):
    x: int
    y: int
    operations: List[str]
    result: int


def callable_one(state: TestState) -> TestState:
    state["x"] = 1
    state["y"] = 1
    state["operations"] = ["add"]

    return state


def callable_two(state):
    if "add" in state["operations"]:
        state["result"] = state["x"] + state["y"]

    return state


test_state: TestState = {"x": 0, "y": 0, "operations": [], "result": 0}

adder_pipe = create_simple_pipe((callable_one, callable_two), state=test_state)
adder_pipe_with_hooks = create_simple_pipe(
    (callable_one, callable_two), state=test_state
)


@pytest.fixture(scope="module")
def pipe_instance() -> SimplePipe[TestState]:
    return adder_pipe


@pytest.fixture(scope="module")
def expected_result():
    return {"x": 1, "y": 1, "operations": ["add"], "result": 2}
