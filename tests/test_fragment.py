import pytest

from graphql_query import Field, Fragment, InlineFragment

from .data import fragment_comparison_fields, fragment_comparison_fields_typename


@pytest.mark.parametrize(
    "fragment, result",
    [
        (fragment_comparison_fields, "fragment comparisonFields on Character {\n  name\n  appearsIn\n}"),
        (
            fragment_comparison_fields_typename,
            "fragment comparisonFields on Character {\n  __typename\n  name\n  appearsIn\n}",
        ),
    ],
)
def test_fragment_from_data(fragment: Fragment, result: str):
    assert fragment.render() == result


def test_fragment():
    fragment = Fragment(
        name="FragmentName",
        type="MyType",
        fields=[
            "name",
            Field(name="field", fields=["f1", "f2", "f3"], typename=True),
            InlineFragment(type="InlineFragmentType", fields=["if1", "if2"], typename=True),
            Fragment(name="FragmentName2", type="MyType2", fields=["frg1", "frg2"], typename=True),
        ],
        typename=True,
    )
    assert (
        fragment.render()
        == """fragment FragmentName on MyType {
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
}"""
    )
