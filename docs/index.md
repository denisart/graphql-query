# graphql-query

[![tag](https://img.shields.io/github/v/tag/denisart/graphql-query)](https://github.com/denisart/graphql-query)
[![last-commit](https://img.shields.io/github/last-commit/denisart/graphql-query/master)](https://github.com/denisart/graphql-query/commits/master)
[![license](https://img.shields.io/github/license/denisart/graphql-query)](https://github.com/denisart/graphql-query/blob/master/LICENSE)

---

**graphql_query** is a complete Domain Specific Language (DSL) for GraphQL query in Python. With this package
you can to

- generate a correct GraphQL query string from a python classes;
- use and share similar Arguments, Variables and e.t.c between different queries;
- easily add new fields to your query;
- add Fragments and Directives to queries;
- generate **graphql_query** classes from pydantic data-model;

The documentation for **graphql_query** can be found at [https://denisart.github.io/graphql-query/](https://denisart.github.io/graphql-query/).

## Quickstart

Install with pip

```bash
pip install graphql_query
```

### Simple query

Code for the simple query

```graphql
{
  hero {
    name
  }
}
```

it is

```python
from graphql_query import Operation, Query

hero = Query(name="hero", fields=["name"])
operation = Operation(type="query", queries=[hero])

print(operation.render())
"""
query {
  hero {
    name
  }
}
"""
```

The `render` method for the `graphql_query.Operation` object
just returns the final string with a query. Inside the `fields` array of the `graphql_query.Query` object
you can use

- `str` (a field name);
- object of `graphql_query.Field` type;
- `graphql_query.Fragment` and `graphql_query.InlineFragment`.

### Arguments, Variables and Directives

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

we can use the following python code

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
            directives=[Directive(name="include", arguments=[arg_if])]
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
"""
query Hero(
  $episode: Episode
  $withFriends: Boolean!
) {
  hero(
    episode: $episode
  ) {
    name
    friends @include(
      if: $withFriends
    ) {
      name
    }
  }
}
"""
```

You can find other examples in the documentation.
