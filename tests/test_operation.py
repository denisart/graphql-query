from typing import List, Optional

import pytest

from graphql_query import Argument, Directive, Field, Fragment, Operation, Query, Variable


@pytest.mark.parametrize(
    "type, name, variables, queries, fragments, result",
    [
        # {
        #   hero {
        #     name
        #   }
        # }
        ("query", None, [], [Query(name="hero", fields=["name"])], [], "query {\n  hero {\n    name\n  }\n}"),
        # {
        #   hero {
        #     name
        #     # Queries can have comments!
        #     friends {
        #       name
        #     }
        #   }
        # }
        (
            "query",
            None,
            [],
            [Query(name="hero", fields=["name", Field(name="friends", fields=["name"])])],
            [],
            "query {\n  hero {\n    name\n    friends {\n      name\n    }\n  }\n}",
        ),
        # {
        #   human(id: "1000") {
        #     name
        #     height
        #   }
        # }
        (
            "query",
            None,
            [],
            [Query(name="human", arguments=[Argument(name="id", value='"1000"')], fields=["name", "height"])],
            [],
            'query {\n  human(\n    id: "1000"\n  ) {\n    name\n    height\n  }\n}',
        ),
        # {
        #   human(id: "1000") {
        #     name
        #     height(unit: FOOT)
        #   }
        # }
        (
            "query",
            None,
            [],
            [
                Query(
                    name="human",
                    arguments=[Argument(name="id", value='"1000"')],
                    fields=["name", Field(name="height", arguments=[Argument(name="unit", value="FOOT")])],
                )
            ],
            [],
            'query {\n  human(\n    id: "1000"\n  ) {\n    name\n    height(\n      unit: FOOT\n    )\n  }\n}',
        ),
        # {
        #   empireHero: hero(episode: EMPIRE) {
        #     name
        #   }
        #   jediHero: hero(episode: JEDI) {
        #     name
        #   }
        # }
        (
            "query",
            None,
            [],
            [
                Query(
                    name="hero",
                    alias="empireHero",
                    arguments=[Argument(name="episode", value='EMPIRE')],
                    fields=["name"],
                ),
                Query(
                    name="hero", alias="jediHero", arguments=[Argument(name="episode", value='JEDI')], fields=["name"]
                ),
            ],
            [],
            '''query {
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
}''',
        ),
        # {
        #   leftComparison: hero(episode: EMPIRE) {
        #     ...comparisonFields
        #   }
        #   rightComparison: hero(episode: JEDI) {
        #     ...comparisonFields
        #   }
        # }
        #
        # fragment comparisonFields on Character {
        #   name
        #   appearsIn
        #   friends {
        #     name
        #   }
        # }
        (
            "query",
            None,
            [],
            [
                Query(
                    name="hero",
                    alias="leftComparison",
                    arguments=[Argument(name="episode", value='EMPIRE')],
                    fields=[
                        Fragment(
                            name="comparisonFields",
                            type="Character",
                            fields=["name", "appearsIn", Field(name="friends", fields=["name"])],
                        )
                    ],
                ),
                Query(
                    name="hero",
                    alias="rightComparison",
                    arguments=[Argument(name="episode", value='JEDI')],
                    fields=[
                        Fragment(
                            name="comparisonFields",
                            type="Character",
                            fields=["name", "appearsIn", Field(name="friends", fields=["name"])],
                        )
                    ],
                ),
            ],
            [
                Fragment(
                    name="comparisonFields",
                    type="Character",
                    fields=["name", "appearsIn", Field(name="friends", fields=["name"])],
                )
            ],
            '''query {
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
}''',
        ),
        # query HeroComparison($first: Int = 3) {
        #   leftComparison: hero(episode: EMPIRE) {
        #     ...comparisonFields
        #   }
        #   rightComparison: hero(episode: JEDI) {
        #     ...comparisonFields
        #   }
        # }
        #
        # fragment comparisonFields on Character {
        #   name
        #   friendsConnection(first: $first) {
        #     totalCount
        #     edges {
        #       node {
        #         name
        #       }
        #     }
        #   }
        # }
        (
            "query",
            "HeroComparison",
            [Variable(name="first", type="Int", default="3")],
            [
                Query(
                    name="hero",
                    alias="leftComparison",
                    arguments=[Argument(name="episode", value='EMPIRE')],
                    fields=[
                        Fragment(
                            name="comparisonFields",
                            type="Character",
                            fields=[
                                "name",
                                Field(
                                    name="friendsConnection",
                                    arguments=[
                                        Argument(name="first", value=Variable(name="first", type="Int", default="3"))
                                    ],
                                    fields=[
                                        "totalCount",
                                        Field(name="edges", fields=[Field(name="node", fields=["name"])]),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                Query(
                    name="hero",
                    alias="rightComparison",
                    arguments=[Argument(name="episode", value='JEDI')],
                    fields=[
                        Fragment(
                            name="comparisonFields",
                            type="Character",
                            fields=[
                                "name",
                                Field(
                                    name="friendsConnection",
                                    arguments=[
                                        Argument(name="first", value=Variable(name="first", type="Int", default="3"))
                                    ],
                                    fields=[
                                        "totalCount",
                                        Field(name="edges", fields=[Field(name="node", fields=["name"])]),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
            ],
            [
                Fragment(
                    name="comparisonFields",
                    type="Character",
                    fields=[
                        "name",
                        Field(
                            name="friendsConnection",
                            arguments=[Argument(name="first", value=Variable(name="first", type="Int", default="3"))],
                            fields=["totalCount", Field(name="edges", fields=[Field(name="node", fields=["name"])])],
                        ),
                    ],
                )
            ],
            '''query HeroComparison(
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
}''',
        ),
        # mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!) {
        #   createReview(episode: $ep, review: $review) {
        #     stars
        #     commentary
        #   }
        # }
        (
            "mutation",
            "CreateReviewForEpisode",
            [Variable(name="ep", type="Episode!"), Variable(name="review", type="ReviewInput!")],
            [
                Query(
                    name="createReview",
                    arguments=[
                        Argument(name="episode", value=Variable(name="ep", type="Episode!")),
                        Argument(name="review", value=Variable(name="review", type="ReviewInput!")),
                    ],
                    fields=["stars", "commentary"],
                ),
            ],
            [],
            '''mutation CreateReviewForEpisode(
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
}''',
        ),
        # query Hero($episode: Episode, $withFriends: Boolean!) {
        #   hero(episode: $episode) {
        #     name
        #     friends @include(if: $withFriends) {
        #       name
        #     }
        #   }
        # }
        (
            "query",
            "Hero",
            [Variable(name="episode", type="Episode"), Variable(name="withFriends", type="Boolean!")],
            [
                Query(
                    name="hero",
                    arguments=[
                        Argument(name="episode", value=Variable(name="episode", type="Episode")),
                    ],
                    fields=[
                        "name",
                        Field(
                            name="friends",
                            fields=["name"],
                            directives=[
                                Directive(
                                    name="include",
                                    arguments=[
                                        Argument(name="if", value=Variable(name="withFriends", type="Boolean!"))
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
            ],
            [],
            '''query Hero(
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
}''',
        ),
        # mutation {
        #   addContent(
        #     title: "ContentTitle",
        #     description: "content description",
        #     active: true,
        #     chapters: [
        #       {
        #         title: "chapter title",
        #         lessons: [
        #           {
        #             title: "lesson title",
        #             filePath: "static-resource-path"
        #           },
        #           {
        #             title: "lesson title 2",
        #             filePath: "static-resource-path2"
        #           }
        #         ]
        #       }
        #     ]
        #   ) {
        #     success
        #   }
        # }
        (
            "mutation",
            None,
            [],
            [
                Query(
                    name="addContent",
                    arguments=[
                        Argument(name="title", value='"ContentTitle"'),
                        Argument(name="description", value='"content description"'),
                        Argument(name="active", value='true'),
                        Argument(
                            name="chapters",
                            value=[
                                [
                                    Argument(name="title", value='"chapter title"'),
                                    Argument(
                                        name="lessons",
                                        value=[
                                            [
                                                Argument(name="title", value='"lesson title"'),
                                                Argument(name="filePath", value='"static-resource-path"'),
                                            ],
                                            [
                                                Argument(name="title", value='"lesson title 2"'),
                                                Argument(name="filePath", value='"static-resource-path 2"'),
                                            ],
                                        ],
                                    ),
                                ]
                            ],
                        ),
                    ],
                    fields=["success"],
                )
            ],
            [],
            """mutation {
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
}""",
        ),
    ],
)
def test_operation(
    type: str,
    name: Optional[str],
    variables: List[Variable],
    queries: List[Query],
    fragments: List[Fragment],
    result: str,
):
    operation = Operation(type=type, name=name, variables=variables, queries=queries, fragments=fragments)

    assert operation.render() == result
