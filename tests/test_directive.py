from typing import List

import pytest

from graphql_query import Argument, Directive, Variable


@pytest.mark.parametrize(
    "name, arguments, result",
    [
        ("skip", [], "@skip"),
        ("skip", [Argument(name="if", value="true")], "@skip(\n  if: true\n)"),
        (
            "include",
            [Argument(name="if", value=Variable(name="withFriends", type="Boolean!"))],
            "@include(\n  if: $withFriends\n)",
        ),
    ],
)
def test_directive(name: str, arguments: List[Argument], result: str):
    assert Directive(name=name, arguments=arguments).render() == result
