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
```
