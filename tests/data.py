from graphql_query import Argument, Field, Fragment, Variable

__all__ = [
    # variables
    "var_first",
    "var_ep",
    "var_review",
    # arguments
    "arg_1",
    "arg_2",
    "arg_episode_jedi",
    "arg_episode_empire",
    "arg_unit",
    "arg_id_1000",
    # fields
    "field_simple",
    "field_simple_typename",
    "field_friends",
    "field_height",
    "field_node",
    "field_friends_connection",
    # fragments
    "fragment_comparison_fields",
    "fragment_comparison_fields_typename",
]


var_first = Variable(name="first", type="Int", default="3")
var_ep = Variable(name="ep", type="Episode!")
var_review = Variable(name="review", type="ReviewInput!")


arg_1 = Argument(name="arg1", value="VALUE1")
arg_2 = Argument(name="arg2", value="VALUE2")
arg_id_1000 = Argument(name="id", value='"1000"')
arg_unit = Argument(name="unit", value="FOOT")
arg_episode_empire = Argument(name="episode", value='EMPIRE')
arg_episode_jedi = Argument(name="episode", value='JEDI')


field_simple = Field(name="field", fields=["f1", "f2", "f3"])
field_simple_typename = Field(name="field", fields=["f1", "f2", "f3"], typename=True)
field_friends = Field(name="friends", fields=["name"])
field_height = Field(name="height", arguments=[arg_unit])
field_node = Field(name="node", fields=["name"])
field_friends_connection = Field(
    name="friendsConnection",
    arguments=[Argument(name="first", value=var_first)],
    fields=["totalCount", Field(name="edges", fields=[field_node])],
)


fragment_comparison_fields = Fragment(
    name="comparisonFields",
    type="Character",
    fields=["name", "appearsIn"],
)
fragment_comparison_fields_typename = Fragment(
    name="comparisonFields",
    type="Character",
    fields=["name", "appearsIn"],
    typename=True,
)
