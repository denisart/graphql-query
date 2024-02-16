# Generate classes from pydantic

We can create **graphql-query** classes from pydantic. For example,

```python
from typing import List
from graphql_query import Field, GraphQLQueryBaseModel

class Friend(GraphQLQueryBaseModel):
    name: str

class Hero(GraphQLQueryBaseModel):
    name: str
    friends: List[Friend]

generated = Hero.graphql_fields()

assert generated == [
    Field(name="name", fields=[]),
    Field(name="friends", fields=[Field(name="name", fields=[])]),
]

Field(name="human", fields=generated).render()
"""human {
  name
  height(
    unit: FOOT
  )
}"""
```

We can use arguments for your queries

```python
from pydantic import Field as PydanticField
from graphql_query import Argument, Field, GraphQLQueryBaseModel

class Human(GraphQLQueryBaseModel):
    name: str
    height: float = PydanticField(
        json_schema_extra={
            "graphql_arguments": [Argument(name="unit", value="FOOT")],
        },
    )

generated = Human.graphql_fields()

assert generated == [
  Field(name="name", fields=[]), Field(name="height", arguments=[Argument(name="unit", value="FOOT")])
]

Field(name="human", fields=generated).render()
"""human {
  name
  height(
    unit: FOOT
  )
}"""
```

For multiply union we have inline fragments

```python
from typing import Union
from graphql_query import Field, GraphQLQueryBaseModel, InlineFragment

class Droid(GraphQLQueryBaseModel):
    primaryFunction: str

class Human(GraphQLQueryBaseModel):
    height: float

class Hero(GraphQLQueryBaseModel):
    name: str
    type: Union[Human, Droid]


generated = Hero.graphql_fields()

Field(name="hero", fields=generated).render()
"""hero {
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
```
