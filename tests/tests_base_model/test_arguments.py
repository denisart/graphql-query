from pydantic import Field as PydanticField

from graphql_query import Argument, Field, GraphQLQueryBaseModel


def test_fields_with_arguments():
    class Human(GraphQLQueryBaseModel):
        name: str
        height: float = PydanticField(
            json_schema_extra={
                "graphql_arguments": [Argument(name="unit", value="FOOT")],
            }
        )

    correct = [Field(name="name", fields=[]), Field(name="height", arguments=[Argument(name="unit", value="FOOT")])]
    generated = Human.graphql_fields()

    assert generated == correct
    assert (
        Field(name="human", fields=generated).render()
        == """human {
  name
  height(
    unit: FOOT
  )
}"""
    )
