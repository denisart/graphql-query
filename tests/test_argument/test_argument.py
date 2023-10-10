import pytest

from graphql_query import Argument, Variable


def test_value_is_str():
    assert Argument(name="arg1", value="VALUE1").render() == "arg1: VALUE1"
    assert Argument(name="id", value='"1000"').render() == 'id: "1000"'
    assert Argument(name="length", value='911').render() == 'length: 911'
    assert Argument(name="unit", value="null").render() == "unit: null"


def test_value_is_int():
    assert Argument(name="length", value=911).render() == 'length: 911'
    assert Argument(name="length", value=0).render() == 'length: 0'
    assert Argument(name="length", value=-1).render() == 'length: -1'


def test_value_is_bool():
    assert Argument(name="some", value=True).render() == 'some: true'
    assert Argument(name="some", value=False).render() == 'some: false'


def test_value_is_float():
    assert Argument(name="some", value=1.0).render() == 'some: 1.0'
    assert Argument(name="some", value=0.2).render() == 'some: 0.2'


def test_value_is_list_str():
    assert Argument(name="someListArgument", value=['"123"']).render() == 'someListArgument: ["123"]'
    assert Argument(name="someListArgument", value=[]).render() == 'someListArgument: []'
    assert Argument(name="someListArgument", value=['"123", "456"']).render() == 'someListArgument: ["123", "456"]'


def test_value_is_list_int():
    assert Argument(name="someListArgument", value=[123]).render() == 'someListArgument: [123]'
    assert Argument(name="someListArgument", value=[]).render() == 'someListArgument: []'
    assert Argument(name="someListArgument", value=[123, 456]).render() == 'someListArgument: [123, 456]'


def test_value_is_list_bool():
    assert Argument(name="someListArgument", value=[True, False]).render() == 'someListArgument: [true, false]'
    assert Argument(name="someListArgument", value=[True]).render() == 'someListArgument: [true]'
    assert Argument(name="someListArgument", value=[False]).render() == 'someListArgument: [false]'


def test_value_is_list_float():
    assert Argument(name="someListArgument", value=[1.0, 0.2]).render() == 'someListArgument: [1.0, 0.2]'
    assert Argument(name="someListArgument", value=[42.0]).render() == 'someListArgument: [42.0]'


@pytest.mark.parametrize(
    "name, value, result",
    [
        ("filter", Argument(name="field", value=123), "filter: {\n  field: 123\n}"),
        ("filter", Argument(name="field", value="VALUE"), "filter: {\n  field: VALUE\n}"),
        ("filter", Argument(name="field", value='"value"'), 'filter: {\n  field: "value"\n}'),
        ("filter", Argument(name="field", value=[123, -456]), "filter: {\n  field: [123, -456]\n}"),
        ("filter", Argument(name="field", value=[42.000, -21.000001]), "filter: {\n  field: [42.0, -21.000001]\n}"),
        (
            "filter",
            Argument(name="field", value=['"value1"', '"value2"']),
            'filter: {\n  field: ["value1", "value2"]\n}',
        ),
        ("filter", Argument(name="field", value=Variable(name="var", type="Variable")), 'filter: {\n  field: $var\n}'),
    ],
)
def test_value_is_argument(name: str, value: Argument, result: str):
    arg = Argument(name=name, value=value)
    assert arg.render() == result


def test_value_is_variable():
    var = Variable(name="var", type="Variable")
    arg = Argument(name="field", value=var)
    assert arg.render() == 'field: $var'


def test_value_is_list_of_args():
    arg = Argument(name="filter", value=[Argument(name="arg1", value="VALUE1"), Argument(name="arg2", value="VALUE2")])
    assert arg.render() == "filter: {\n  arg1: VALUE1\n  arg2: VALUE2\n}"


def test_value_is_args_with_args():
    arg = Argument(
        name="filter1",
        value=[
            Argument(
                name="filter2", value=[Argument(name="arg1", value="VALUE1"), Argument(name="arg2", value="VALUE2")]
            )
        ],
    )
    assert arg.render() == "filter1: {\n  filter2: {\n    arg1: VALUE1\n    arg2: VALUE2\n  }\n}"


def test_value_long():
    arg = Argument(
        name="filter1",
        value=[
            Argument(
                name="filter2",
                value=[
                    Argument(name="arg1", value="VALUE1"),
                    Argument(name="filter3", value=Argument(name="arg2", value="VALUE2")),
                ],
            )
        ],
    )
    assert (
        arg.render()
        == """filter1: {
  filter2: {
    arg1: VALUE1
    filter3: {
      arg2: VALUE2
    }
  }
}"""
    )


def test_value_if_list_of_list_of_args():
    arg = Argument(
        name="lessons",
        value=[
            [Argument(name="title", value='"lesson title"'), Argument(name="filePath", value='"static-resource-path"')],
            [
                Argument(name="title", value='"lesson title 2"'),
                Argument(name="filePath", value='"static-resource-path 2"'),
            ],
        ],
    )
    assert (
        arg.render()
        == """lessons: [
  {
    title: "lesson title"
    filePath: "static-resource-path"
  }
  {
    title: "lesson title 2"
    filePath: "static-resource-path 2"
  }
]"""
    )
