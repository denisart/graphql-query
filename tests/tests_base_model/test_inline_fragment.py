from typing import Union

from graphql_query import Field, GraphQLQueryBaseModel, InlineFragment


def test_inline_fragments():
    class Droid(GraphQLQueryBaseModel):
        primaryFunction: str

    class Human(GraphQLQueryBaseModel):
        height: float

    class Hero(GraphQLQueryBaseModel):
        name: str
        type: Union[Human, Droid]

    correct = [
        Field(name="name", fields=[]),
        Field(
            name="type",
            fields=[
                InlineFragment(type="Human", fields=[Field(name="height", fields=[])]),
                InlineFragment(type="Droid", fields=[Field(name="primaryFunction", fields=[])]),
            ],
        ),
    ]
    generated = Hero.graphql_fields()

    assert generated == correct
    assert (
        Field(name="hero", fields=generated).render()
        == """hero {
  name
  type {
    ... on Human {
      height
    }
    ... on Droid {
      primaryFunction
    }
  }
}"""
    )
