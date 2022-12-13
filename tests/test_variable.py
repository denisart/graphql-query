from typing import Optional

import pytest

from graphql_query import Variable

from .data import var_ep, var_first, var_review


@pytest.mark.parametrize(
    "name, var_type, default, result",
    [
        ("episode", "Episode", None, "$episode: Episode"),
        ("episode", "Episode", "JEDI", "$episode: Episode = JEDI"),
        ("episode_id", "ID!", '"123-456"', '$episode_id: ID! = "123-456"'),
    ]
)
def test_variable(name: str, var_type: str, default: Optional[str], result: str):
    var = Variable(name=name, type=var_type, default=default)
    assert var.render() == result


@pytest.mark.parametrize(
    "var, result",
    [
        (var_ep, "$ep: Episode!"),
        (var_first, "$first: Int = 3"),
        (var_review, "$review: ReviewInput!"),
    ]
)
def test_variable_from_data(var: Variable, result: str):
    assert var.render() == result
