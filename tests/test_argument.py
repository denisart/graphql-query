from typing import List, Union

import pytest

from graphql_query import Argument, Variable

from .data import arg_1, arg_2, arg_episode_empire, arg_episode_jedi, arg_id_1000, arg_unit


@pytest.mark.parametrize(
    'arg, result',
    [
        (arg_1, "arg1: VALUE1"),
        (arg_2, "arg2: VALUE2"),
        (arg_episode_empire, "episode: EMPIRE"),
        (arg_episode_jedi, "episode: JEDI"),
        (arg_unit, "unit: FOOT"),
        (arg_id_1000, 'id: "1000"'),
    ]
)
def test_argument_from_data(arg: Argument, result: str):
    assert arg.render() == result


@pytest.mark.parametrize(
    'name, value, result',
    [
        ("filter", Argument(name="field", value="VALUE"), "filter: {\n  field: VALUE\n}"),
        ("filter", Argument(name="field", value='"value"'), 'filter: {\n  field: "value"\n}'),
        (
            "filter",
            Argument(name="field", value=Variable(name="var", type="Variable")),
            "filter: {\n  field: $var\n}"
        ),
        (
            "filter",
            [arg_1, arg_2],
            "filter: {\n  arg1: VALUE1\n  arg2: VALUE2\n}"
        ),
        (
            "filter1",
            Argument(
                name="filter2",
                value=[arg_1, arg_2],
            ),
            "filter1: {\n  filter2: {\n    arg1: VALUE1\n    arg2: VALUE2\n  }\n}"
        ),
        (
            "filter1",
            Argument(
                name="filter2",
                value=[arg_1, Argument(name="filter3", value=arg_2)],
            ),
            """filter1: {
  filter2: {
    arg1: VALUE1
    filter3: {
      arg2: VALUE2
    }
  }
}"""
        ),

    ]
)
def test_argument(name: str, value: Union[str, Argument, List[Argument], Variable], result: str):
    arg = Argument(name=name, value=value)
    assert arg.render() == result
