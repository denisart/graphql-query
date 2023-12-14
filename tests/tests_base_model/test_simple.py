from typing import List

from graphql_query import Field, GraphQLQueryBaseModel


def test_simple_model():
    class Friend(GraphQLQueryBaseModel):
        name: str

    class Hero(GraphQLQueryBaseModel):
        name: str
        friends: List[Friend]

    correct = [
        Field(name="name", fields=[]),
        Field(name="friends", fields=[Field(name="name", fields=[])]),
    ]
    generated = Hero.graphql_fields()

    assert generated == correct
    assert (
        Field(name="hero", fields=generated).render()
        == """hero {
  name
  friends {
    name
  }
}"""
    )
