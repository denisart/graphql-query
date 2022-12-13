# GraphQL-Query

[![Build](https://img.shields.io/github/workflow/status/denisart/graphql-query/Code%20checking)](https://github.com/denisart/graphql-query/actions)
[![tag](https://img.shields.io/github/v/tag/denisart/graphql-query)](https://github.com/denisart/graphql-query)
[![last-commit](https://img.shields.io/github/last-commit/denisart/graphql-query/master)](https://github.com/denisart/graphql-query/commits/master)
[![license](https://img.shields.io/github/license/denisart/graphql-query)](https://github.com/denisart/graphql-query/blob/master/LICENSE)

**graphql_query** is python classes for generating GraphQL queries.
The documentation for **graphql_query** can be found at [https://denisart.github.io/graphql_query](https://denisart.github.io/graphql_query).

## Quickstart

Install with pip

```bash
pip install graphql_query
```

For generation of the following query

```graphql
query Hero($episode: Episode, $withFriends: Boolean!) {
  hero(episode: $episode) {
    name
    friends @include(if: $withFriends) {
      name
    }
  }
}
```

we have

```python
from graphql_query import Argument, Directive, Field, Operation, Query, Variable

episode = Variable(name="episode", type="Episode")
withFriends = Variable(name="withFriends", type="Boolean!")

arg_episode = Argument(name="episode", value=episode)
arg_if = Argument(name="if", value=withFriends)

hero = Query(
    name="hero",
    arguments=[arg_episode],
    fields=[
        "name",
        Field(
            name="friends",
            fields=["name"],
            directives=[
                Directive(
                    name="include",
                    arguments=[arg_if]
                )
            ]
        )
    ]
)
operation = Operation(
    type="query",
    name="Hero",
    variables=[episode, withFriends],
    queries=[hero]
)
print(operation.render())
# query Hero(
#   $episode: Episode
#   $withFriends: Boolean!
# ) {
#   hero(
#     episode: $episode
#   ) {
#     name
#     friends @include(
#       if: $withFriends
#     ) {
#       name
#     }
#   }
# }
```