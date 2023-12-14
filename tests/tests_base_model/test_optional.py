from datetime import datetime
from typing import Optional

from graphql_query import Field, GraphQLQueryBaseModel


def test_optional():
    class Author(GraphQLQueryBaseModel):
        login: str
        avatarUrl: str
        url: str

    class CommentsNode(GraphQLQueryBaseModel):
        createdAt: datetime
        author: Optional[Author] = None

    correct = [
        Field(name="createdAt", fields=[]),
        Field(
            name="author",
            fields=[
                Field(name="login", fields=[]),
                Field(name="avatarUrl", fields=[]),
                Field(name="url", fields=[]),
            ],
        ),
    ]
    generated = CommentsNode.graphql_fields()

    assert generated == correct
    assert (
        Field(name="comments", fields=generated).render()
        == """comments {
  createdAt
  author {
    login
    avatarUrl
    url
  }
}"""
    )
