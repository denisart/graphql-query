from typing import List, Optional, Union

import pytest

from graphql_query import Argument, Field, Fragment, InlineFragment, Query

from .data import arg_1, arg_2, arg_id_1000, field_simple_typename


@pytest.mark.parametrize(
    "name, alias, arguments, typename, fields, result",
    [
        ("human", None, [arg_id_1000], False, ["name", "height"], 'human(\n  id: "1000"\n) {\n  name\n  height\n}'),
        (
            "human",
            "human1000th",
            [arg_id_1000],
            False,
            ["name", "height"],
            'human1000th: human(\n  id: "1000"\n) {\n  name\n  height\n}',
        ),
        ("human", "human1000th", [], False, ["name", "height"], 'human1000th: human {\n  name\n  height\n}'),
        (
            "human",
            "human1000th",
            [arg_id_1000],
            True,
            ["name", "height"],
            'human1000th: human(\n  id: "1000"\n) {\n  __typename\n  name\n  height\n}',
        ),
        (
            "human",
            None,
            [Argument(name="filter", value=[arg_1, arg_2])],
            False,
            ["name", "height"],
            'human(\n  filter: {\n    arg1: VALUE1\n    arg2: VALUE2\n  }\n) {\n  name\n  height\n}',
        ),
        (
            "my_query",
            "my_alias",
            [],
            True,
            [
                "name",
                field_simple_typename,
                InlineFragment(type="InlineFragmentType", fields=["if1", "if2"], typename=True),
                Fragment(name="FragmentName2", type="MyType2", fields=["frg1", "frg2"], typename=True),
            ],
            """my_alias: my_query {
  __typename
  name
  field {
    __typename
    f1
    f2
    f3
  }
  ... on InlineFragmentType {
    __typename
    if1
    if2
  }
  ...FragmentName2
}""",
        ),
    ],
)
def test_query(
    name: str,
    alias: Optional[str],
    arguments: List[Argument],
    typename: bool,
    fields: List[Union[str, Field, InlineFragment, Fragment]],
    result: str,
):
    query = Query(name=name, alias=alias, arguments=arguments, typename=typename, fields=fields)

    assert query.render() == result
