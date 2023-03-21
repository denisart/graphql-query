from typing import List, Optional, Union

import pytest

from graphql_query import Argument, Directive, Field, Fragment, InlineFragment, Variable

from .data import (
    arg_1,
    arg_2,
    field_friends,
    field_friends_connection,
    field_height,
    field_node,
    field_simple,
    field_simple_typename,
)


@pytest.mark.parametrize(
    "field, result",
    [
        (field_simple, "field {\n  f1\n  f2\n  f3\n}"),
        (field_simple_typename, "field {\n  __typename\n  f1\n  f2\n  f3\n}"),
        (field_node, "node {\n  name\n}"),
        (field_height, "height(\n  unit: FOOT\n)"),
        (field_friends, "friends {\n  name\n}"),
        (
            field_friends_connection,
            """friendsConnection(
  first: $first
) {
  totalCount
  edges {
    node {
      name
    }
  }
}""",
        ),
    ],
)
def test_field_from_data(field: Field, result: str):
    assert field.render() == result


@pytest.mark.parametrize(
    "name, alias, arguments, fields, typename, result",
    [
        ("name", None, [], [], False, "name"),
        ("name", "my_name", [], [], False, "my_name: name"),
        ("field", None, [arg_1, arg_2], [], False, "field(\n  arg1: VALUE1\n  arg2: VALUE2\n)"),
        (
            "field",
            None,
            [Argument(name="filter", value=[arg_1, arg_2])],
            [],
            False,
            "field(\n  filter: {\n    arg1: VALUE1\n    arg2: VALUE2\n  }\n)",
        ),
        (
            "field1",
            None,
            [],
            [field_simple_typename],
            True,
            "field1 {\n  __typename\n  field {\n    __typename\n    f1\n    f2\n    f3\n  }\n}",
        ),
        (
            "field1",
            None,
            [],
            [Fragment(name="MyFragment", type="MyType", fields=["f1"])],
            True,
            "field1 {\n  __typename\n  ...MyFragment\n}",
        ),
    ],
)
def test_field(
    name: str,
    alias: Optional[str],
    arguments: List[Argument],
    fields: List[Union[str, 'Field', 'InlineFragment', 'Fragment']],
    typename: bool,
    result: str,
):
    field = Field(name=name, alias=alias, arguments=arguments, fields=fields, typename=typename)
    assert field.render() == result


def test_field_with_directive():
    field = Field(
        name="friends",
        fields=["name"],
        directives=[
            Directive(
                name="include", arguments=[Argument(name="if", value=Variable(name="withFriends", type="Boolean!"))]
            )
        ],
    )

    assert (
        field.render()
        == '''friends @include(
  if: $withFriends
) {
  name
}'''
    )


def test_field_with_two_directives():
    field = Field(
        name="friends",
        fields=["name"],
        directives=[
            Directive(name="include", arguments=[Argument(name="if", value="true")]),
            Directive(name="skip", arguments=[Argument(name="if", value="false")]),
        ],
    )

    assert (
        field.render()
        == '''friends @include(
  if: true
) @skip(
  if: false
) {
  name
}'''
    )
