# List of Objects

It is an example for GraphQL query generation from some python dict.

Let's say we want to generate the following mutation

```graphql
mutation {
  addContent(
    title: "ContentTitle"
    description: "content description"
    active: true
    chapters: [
      {
        title: "chapter title"
        lessons: [
          {
            title: "lesson title"
            filePath: "static-resource-path"
          }
          {
            title: "lesson title 2"
            filePath: "static-resource-path2"
          }
        ]
      }
    ]
  ) {
    success
  }
}
```

from the following dict

```python
example_dict = {
    'title': 'ContentTitle',
    'description': 'content description',
    'active': True,
    'chapters': [
        {
            'title': 'chapter title',
            'lessons': [
                {
                    'title': 'lesson title',
                    'filePath': 'static-resource-path'
                },
                {
                    'title': 'lesson title 2',
                    'filePath': 'static-resource-path2'
                }
            ]
        }
    ]
}
```


The following code it is a simple realisation of this problem

```python
from typing import Any, Dict, List
from graphql_query import Argument, Operation, Query

def scalar_argument(key: str, value: Any) -> Argument:
    """Generate an Argument in the following form

    key: "value"
    key: true
    key: false
    ...

    """

    if isinstance(value, str):
        return Argument(name=key, value=f'"{value}"')

    elif isinstance(value, bool):
        return Argument(name=key, value=str(value).lower())

    # your cases here...

def get_query_arguments(arguments_dict: Dict[str, Any]) -> List[Argument]:
    query_arguments = []

    for key, value in arguments_dict.items():
        # processing of scalar values
        if isinstance(value, str) or isinstance(value, bool):
            query_arguments.append(scalar_argument(key, value))

        # processing of list with objects
        elif isinstance(value, list):
            values = [get_query_arguments(obj) for obj in value]
            query_arguments.append(Argument(name=key, value=values))

    return query_arguments

target_mutation = Operation(
    type="mutation",
    queries=[
        Query(
            name="addContent",
            arguments=get_query_arguments(example_dict),
            fields=["success"]
        )
    ]
)

print(target_mutation.render())
"""
mutation {
  addContent(
    title: "ContentTitle"
    description: "content description"
    active: true
    chapters: [
      {
        title: "chapter title"
        lessons: [
          {
            title: "lesson title"
            filePath: "static-resource-path"
          }
          {
            title: "lesson title 2"
            filePath: "static-resource-path2"
          }
        ]
      }
    ]
  ) {
    success
  }
}
"""
```