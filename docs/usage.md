# How to use

**graphql_query** provides special python classes for generate of GraphQL queries.
Below are examples of using these classes for queries from GraphQL documentation
https://graphql.org/learn/queries/

## First query

**Operation** it is the general class for render of your GraphQL query or mutation.
For the first query from https://graphql.org/learn/queries/#fields

```graphql
{
  hero {
    name
  }
}
```

we can to use **graphql_query.Operation** as like that

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

Same way for the query with sub-fields

```python
"""
{
  hero {
    name
    # Queries can have comments!
    friends {
      name
    }
  }
}
"""
```

we can to use **graphql_query.Field** as like that

```python
from graphql_query import Field, Operation, Query

hero = Query(
    name="hero",
    fields=[
        "name",
        Field(name="friends", fields=["name"])
    ]
)
operation = Operation(type="query", queries=[hero])

print(operation.render())
"""
query {
  hero {
    name
    friends {
      name
    }
  }
}
"""
```

## Arguments

For arguments in your query or fields (https://graphql.org/learn/queries/#arguments)
you can use **graphql_query.Argument**:

```python
from graphql_query import Argument, Operation, Query, Field

human = Query(
    name="human",
    arguments=[Argument(name="id", value='"1000"')],
    fields=[
        "name",
        Field(
            name="height",
            arguments=[Argument(name="unit", value="FOOT")]
        )
    ]
)
operation = Operation(type="query", queries=[human])

print(operation.render())
"""
query {
  human(
    id: "1000"
  ) {
    name
    height(
      unit: FOOT
    )
  }
}
"""
```

## Aliases

**graphql_query.Query** has the special field for alias

```python
from graphql_query import Argument, Operation, Query

empireHero = Query(
    name="hero",
    alias="empireHero",
    arguments=[Argument(name="episode", value="EMPIRE")],
    fields=["name"]
)

jediHero = Query(
    name="hero",
    alias="jediHero",
    arguments=[Argument(name="episode", value="JEDI")],
    fields=["name"]
)

operation = Operation(type="query", queries=[empireHero, jediHero])
print(operation.render())
"""
query {
  empireHero: hero(
    episode: EMPIRE
  ) {
    name
  }
    jediHero: hero(
    episode: JEDI
  ) {
    name
  }
}
"""
```

## Fragments

Fragment is the power of GraphQL. Use **graphql_query.Fragment** with
**graphql_query.Operation.fragments**:

```python
from graphql_query import Argument, Operation, Query, Fragment, Field

comparisonFields = Fragment(
    name="comparisonFields",
    type="Character",
    fields=["name", "appearsIn", Field(name="friends", fields=["name"])]
)

leftComparison = Query(
    name="hero",
    alias="leftComparison",
    arguments=[Argument(name="episode", value="EMPIRE")],
    fields=[comparisonFields]
)

rightComparison = Query(
    name="hero",
    alias="rightComparison",
    arguments=[Argument(name="episode", value="JEDI")],
    fields=[comparisonFields]
)

operation = Operation(
    type="query",
    queries=[leftComparison, rightComparison],
    fragments=[comparisonFields]
)
print(operation.render())
"""
query {
  leftComparison: hero(
    episode: EMPIRE
  ) {
    ...comparisonFields
  }

  rightComparison: hero(
    episode: JEDI
  ) {
    ...comparisonFields
  }
}

fragment comparisonFields on Character {
  name
  appearsIn
  friends {
    name
  }
}
"""
```

## Using variables inside fragments

Variables can also be used in fragments

```python
from graphql_query import Argument, Operation, Query, Fragment, Field, Variable

var_first = Variable(name="first", type="Int", default="3")

comparisonFields = Fragment(
    name="comparisonFields",
    type="Character",
    fields=[
        "name",
        Field(
            name="friendsConnection",
            arguments=[Argument(name="first", value=var_first)],
            fields=[
                "totalCount",
                Field(
                    name="edges",
                    fields=[
                        Field(name="node", fields=["name"])
                    ]
                )
            ]
        )
    ]
)

leftComparison = Query(
    name="hero",
    alias="leftComparison",
    arguments=[Argument(name="episode", value="EMPIRE")],
    fields=[comparisonFields]
)

rightComparison = Query(
    name="hero",
    alias="rightComparison",
    arguments=[Argument(name="episode", value="JEDI")],
    fields=[comparisonFields]
)

operation = Operation(
    type="query",
    name="HeroComparison",
    queries=[leftComparison, rightComparison],
    fragments=[comparisonFields],
    variables=[var_first]
)
print(operation.render())
"""
query HeroComparison(
  $first: Int = 3
) {
  leftComparison: hero(
    episode: EMPIRE
  ) {
    ...comparisonFields
  }

  rightComparison: hero(
    episode: JEDI
  ) {
    ...comparisonFields
  }
}

fragment comparisonFields on Character {
  name
  friendsConnection(
    first: $first
  ) {
    totalCount
    edges {
      node {
        name
      }
    }
  }
}
"""
```

## Operation name

Here’s an example that includes the keyword query as operation type and
HeroNameAndFriends as operation name:

```python
from graphql_query import Operation, Query, Field

hero = Query(
    name="hero",
    fields=["name", Field(name="friends", fields=["name"])]
)

operation = Operation(
    type="query",
    name="HeroNameAndFriends",
    queries=[hero],
)
print(operation.render())
"""
query HeroNameAndFriends {
  hero {
    name
    friends {
      name
    }
  }
}
"""
```

## Directives

If you use directives in your queries then using **graphql_query.Directive**

```python
from graphql_query import Argument, Directive, Operation, Query, Field, Variable

var_episode = Variable(name="episode", type="Episode")
var_withFriends = Variable(name="withFriends", type="Boolean!")

hero = Query(
    name="hero",
    arguments=[Argument(name="episode", value=var_episode))]
    fields=[
        "name",
        Field(
            name="friends",
            directives=[
                Directive(name="include", arguments=[
                    Argument(name="if", value=var_withFriends)
                ])
            ]
            fields=["name"]
        )
    ]
)

operation = Operation(
    type="query",
    name="Hero",
    queries=[hero],
    variables=[var_episode, var_withFriends]
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

## Mutations

Creating mutation is the same as creating query

```python
from graphql_query import Argument, Operation, Query, Variable

ep = Variable(name="ep", type="Episode!")
review = Variable(name="review", type="ReviewInput!")

createReview = Query(
    name="createReview",
    arguments=[
        Argument(name="episode", value=ep),
        Argument(name="review", value=review),
    ],
    fields=["stars", "commentary"]
)

operation = Operation(
    type="mutation",
    name="CreateReviewForEpisode",
    variables=[ep, review],
    queries=[createReview],
)
print(operation.render())
"""
mutation CreateReviewForEpisode(
  $ep: Episode!
  $review: ReviewInput!
) {
  createReview(
    episode: $ep
    review: $review
  ) {
    stars
    commentary
  }
}
"""
```

## Inline Fragments

For union types you can use inline fragments https://graphql.org/learn/queries/#inline-fragments

```python
from graphql_query import Argument, Operation, Query, Variable, InlineFragment

ep = Variable(name="ep", type="Episode!")

hero = Query(
    name="hero",
    arguments=[
        Argument(name="episode", value=ep),
    ],
    fields=[
        "stars",
        InlineFragment(type="Droid", fields=["primaryFunction"]),
        InlineFragment(type="Human", fields=["height"]),
    ]
)

operation = Operation(
    type="query",
    name="HeroForEpisode",
    variables=[ep],
    queries=[hero],
)
print(operation.render())
"""
query HeroForEpisode(
  $ep: Episode!
) {
  hero(
    episode: $ep
  ) {
    stars
    ... on Droid {
      primaryFunction
    }
    ... on Human {
      height
    }
  }
}
"""
```

## Meta fields

Typename of fields

```python
from graphql_query import Argument, Operation, Query, InlineFragment

search = Query(
    name="search",
    arguments=[Argument(name="text", value='"an"')],
    typename=True,
    fields=[
        InlineFragment(type="Droid", fields=["name"]),
        InlineFragment(type="Human", fields=["name"]),
        InlineFragment(type="Starship", fields=["name"]),
    ]
)

operation = Operation(
    type="query",
    queries=[search],
)
print(operation.render())
"""
query {
  search(
    text: "an"
  ) {
    __typename
    ... on Droid {
      name
    }
    ... on Human {
      name
    }
    ... on Starship {
      name
    }
  }
}
"""
```

## Argument as list of objects

If you have an argument as list of objects

```graphql
mutation {
  addContent(
    title: "ContentTitle",
    description: "content description",
    active: true,
    chapters: [
      {
        title: "chapter title",
        lessons: [
          {
            title: "lesson title",
            filePath: "static-resource-path"
          },
          {
            title: "lesson title 2",
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

You can to render this case as well

```python
from graphql_query import Argument

content_title = Argument(name="title", value='"ContentTitle"')
description = Argument(name="description", value='"content description"')
active = Argument(name="active", value='true')

chapters = Argument(
    name="chapters",
    value=[
        # list with list of arguments
        [
            Argument(name="title", value='"chapter title"'),
            Argument(
                name="lessons",
                value=[
                    # list with list of arguments
                    [
                        Argument(name="title", value='"lesson title"'),
                        Argument(name="filePath", value='"static-resource-path"'),
                    ],
                    [
                        Argument(name="title", value='"lesson title 2"'),
                        Argument(name="filePath", value='"static-resource-path 2"'),
                    ]
                ]
            )
        ]
    ]
)

addContent = Query(
    name="addContent",
    arguments=[
        content_title, description, active, chapters
    ],
    fields=["success"]
)
operation = Operation(type="mutation", queries=[addContent])

print(operation.render())
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
            filePath: "static-resource-path 2"
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