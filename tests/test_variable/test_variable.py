from typing import Optional

import pytest

from graphql_query import Variable


@pytest.mark.parametrize(
    "name, var_type, default, result",
    [
        ("episode", "Episode", None, "$episode: Episode"),
        ("episode", "Episode", "JEDI", "$episode: Episode = JEDI"),
        ("episode_id", "ID!", '"123-456"', '$episode_id: ID! = "123-456"'),
    ],
)
def test_variable(name: str, var_type: str, default: Optional[str], result: str):
    var = Variable(name=name, type=var_type, default=default)
    assert var.render() == result


@pytest.mark.parametrize(
    "var, result",
    [
        (Variable(name="ep", type="Episode!"), "$ep: Episode!"),
        (Variable(name="first", type="Int", default="3"), "$first: Int = 3"),
        (Variable(name="review", type="ReviewInput!"), "$review: ReviewInput!"),
    ],
)
def test_variable_from_data(var: Variable, result: str):
    assert var.render() == result
