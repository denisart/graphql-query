from typing import List, Union

import pytest

from graphql_query import Argument, Field, Fragment, InlineFragment

from .data import arg_1, arg_2, field_simple_typename


@pytest.mark.parametrize(
    "type, arguments, fields, typename, result",
    [
        ("name", [], ["f1", "f2", "f3"], False, "... on name {\n  f1\n  f2\n  f3\n}"),
        ("name", [], ["f1", "f2", "f3"], True, "... on name {\n  __typename\n  f1\n  f2\n  f3\n}"),
        (
            "type",
            [arg_1, arg_2],
            ["f1", "f2", "f3"],
            False,
            "... on type(\n  arg1: VALUE1\n  arg2: VALUE2\n) {\n  f1\n  f2\n  f3\n}",
        ),
        (
            "type",
            [Argument(name="filter", value=[arg_1, arg_2])],
            ["f1", "f2", "f3"],
            False,
            "... on type(\n  filter: {\n    arg1: VALUE1\n    arg2: VALUE2\n  }\n) {\n  f1\n  f2\n  f3\n}",
        ),
        (
            "type",
            [],
            [field_simple_typename],
            True,
            "... on type {\n  __typename\n  field {\n    __typename\n    f1\n    f2\n    f3\n  }\n}",
        ),
        (
            "type",
            [],
            [Fragment(name="MyFragment", type="MyType", fields=["f1"])],
            True,
            "... on type {\n  __typename\n  ...MyFragment\n}",
        ),
    ],
)
def test_inline_fragment(
    type: str,
    arguments: List[Argument],
    fields: List[Union[str, Field, InlineFragment, Fragment]],
    typename: bool,
    result: str,
):
    fragment = InlineFragment(type=type, arguments=arguments, fields=fields, typename=typename)
    assert fragment.render() == result
