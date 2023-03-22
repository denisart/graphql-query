import pytest

from graphql_query.types import _GraphQL2PythonQuery


def test_line_shift():
    assert _GraphQL2PythonQuery._line_shift("aaabbbccc") == "aaabbbccc"
    assert _GraphQL2PythonQuery._line_shift("aaa\nbbb\nccc") == "aaa\n  bbb\n  ccc"


def test_render_not_implemented():
    class A(_GraphQL2PythonQuery):
        pass

    with pytest.raises(NotImplementedError):
        a = A()
        a.render()
