from typing import Any, TypedDict

from pipe_framework.core.base import Hooks, SimplePipe

def run_simple(pipe: SimplePipe, hooks: Hooks) -> TypedDict: ...
