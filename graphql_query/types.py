import os
import sys
from pathlib import Path
from typing import Any, List, Optional, Union

from jinja2 import Environment, FileSystemLoader, Template
from pydantic.v1 import BaseModel
from pydantic.v1 import Field as PydanticField

if sys.version_info >= (3, 10):
    from typing import TypeGuard
else:
    # Use TypeGuard from typing_extensions for python <= 3.9
    from typing_extensions import TypeGuard

__all__ = [
    "Variable",
    "Argument",
    "Directive",
    "Field",
    "InlineFragment",
    "Fragment",
    "Query",
    "Operation",
]


# templates setting for render of classes
TEMPLATES_FOLDER = Path(os.path.join(os.path.dirname(__file__), "templates/"))

template_env = Environment(loader=FileSystemLoader(searchpath=TEMPLATES_FOLDER))


class _GraphQL2PythonQuery(BaseModel):
    """An abstract class for GraphQL query type."""

    class Config:
        # pylint: disable=too-few-public-methods
        smart_union = True
        extra = "forbid"
        arbitrary_types_allowed = True
        allow_reuse = True

    @staticmethod
    def _line_shift(text: str) -> str:
        return "\n  ".join(text.split("\n"))

    def _render_field(self, field: Union[str, 'Field', 'InlineFragment', 'Fragment']) -> str:
        if isinstance(field, str):
            return field

        if isinstance(field, Fragment):
            return f"...{field.name}"

        return self._line_shift(field.render())

    def render(self) -> str:
        raise NotImplementedError


class Variable(_GraphQL2PythonQuery):
    """GraphQL variable type.

    See https://graphql.org/learn/queries/#variables for more details.

    Attributes:
        name: A name of the variable.
        type: A GraphQL type of the variable.
        default: A default value for the variable.

    Example:

        In the query

        >>> query_str = '''
        ... query HeroNameAndFriends($episode: Episode = JEDI) {
        ...   hero(episode: $episode) {
        ...     name
        ...     friends {
        ...       name
        ...     }
        ...   }
        ... }
        ... '''

        we have the following variable:

        >>> var_episode = Variable(name="episode", type="Episode", default="JEDI")

    """

    name: str
    type: str
    default: Optional[str] = PydanticField(default=None)

    _template: Template = template_env.get_template("variable.jinja2")

    def render(self) -> str:
        return self._template.render(name=self.name, type=self.type, default=self.default)


class Argument(_GraphQL2PythonQuery):
    """GraphQL argument type.

    See https://graphql.org/learn/queries/#arguments for more details.

    Attributes:
        name: A name of the argument.
        value: The argument value.

    Example 1:

        In the query

        >>> query_string = '''
        ... {
        ...   human(id: "1000") {
        ...     name
        ...     height(unit: FOOT)
        ...   }
        ... }
        ... '''

        we have two arguments

        >>> arg_id = Argument(name="id", value='"1000"')
        >>> arg_unit = Argument(name="unit", value='FOOT')

    Example 2:

        In the query

        >>> query_string = '''
        ... {
        ...   q(
        ...     filter1: {
        ...       filter2: {
        ...         field1: "value1"
        ...          field2: VALUE2
        ...        }
        ...      }
        ...   ) {
        ...     ...
        ...   }
        ... }
        ... '''

        we have the long argument

        >>> filter1 = Argument(
        ...     name="filter1",
        ...     value=Argument(
        ...         name="filter2",
        ...         value=[
        ...             Argument(name="field1", value='"value1"'),
        ...             Argument(name="field2", value='VALUE2'),
        ...         ]
        ...     )
        ... )

    """

    name: str
    value: Union[
        str,
        int,
        'Argument',
        Variable,
        List[str],
        List[int],
        List['Argument'],
        List[List['Argument']],
    ]

    _template_key_value: Template = template_env.get_template("argument_key_value.jinja2")
    _template_key_values: Template = template_env.get_template("argument_key_values.jinja2")
    _template_key_argument: Template = template_env.get_template("argument_key_argument.jinja2")
    _template_key_variable: Template = template_env.get_template("argument_key_variable.jinja2")
    _template_key_arguments: Template = template_env.get_template("argument_key_arguments.jinja2")
    _template_key_objects: Template = template_env.get_template("argument_key_objects.jinja2")

    @staticmethod
    def _check_is_list_of_str(values: List[Any]) -> TypeGuard[List[str]]:
        return all(isinstance(value, str) for value in values)

    @staticmethod
    def _check_is_list_of_arguments(values: List[Any]) -> TypeGuard[List['Argument']]:
        return all(isinstance(value, Argument) for value in values)

    @staticmethod
    def _check_is_list_of_list(values: List[Any]) -> TypeGuard[List[List[Any]]]:
        return all(isinstance(value, list) for value in values)

    def _render_for_str(self, name: str, value: str) -> str:
        return self._template_key_value.render(name=name, value=value)

    def _render_for_int(self, name: str, value: int) -> str:
        return self._template_key_value.render(name=name, value=str(value))

    def _render_for_argument(self, name: str, value: 'Argument') -> str:
        return self._template_key_argument.render(name=name, argument=self._line_shift(value.render()))

    def _render_for_list_str(self, name: str, value: List[str]) -> str:
        return self._template_key_values.render(name=name, values=value)

    def _render_for_list_argument(self, name: str, value: List['Argument']) -> str:
        return self._template_key_arguments.render(
            name=name, arguments=[self._line_shift(argument.render()) for argument in value]
        )

    def _render_for_list_list_argument(self, name: str, value: List[List['Argument']]) -> str:
        return self._template_key_objects.render(
            name=name,
            list_arguments=[
                [self._line_shift(self._line_shift(argument.render())) for argument in arguments] for arguments in value
            ],
        )

    def _render_for_variable(self, name: str, value: Variable) -> str:
        return self._template_key_variable.render(name=name, value=value.name)

    def render(self) -> str:
        if isinstance(self.value, str):
            return self._render_for_str(self.name, self.value)

        if isinstance(self.value, int):
            return self._render_for_int(self.name, self.value)

        if isinstance(self.value, Argument):
            return self._render_for_argument(self.name, self.value)

        if isinstance(self.value, Variable):
            return self._render_for_variable(self.name, self.value)

        if isinstance(self.value, list):
            if self._check_is_list_of_str(self.value):
                return self._render_for_list_str(self.name, self.value)

            if self._check_is_list_of_arguments(self.value):
                return self._render_for_list_argument(self.name, self.value)

            if self._check_is_list_of_list(self.value):
                if all(self._check_is_list_of_arguments(v) for v in self.value):
                    return self._render_for_list_list_argument(self.name, self.value)

        raise ValueError("Invalid type for `graphql_query.Argument.value`.")


class Directive(_GraphQL2PythonQuery):
    """GraphQL directive type.

    See https://graphql.org/learn/queries/#directives for more details.

    Attributes:
        name: A directive name.
        arguments: Directive arguments.

    Example:

        In the query

        >>> query_str = '''
        ... query Hero($episode: Episode, $withFriends: Boolean!) {
        ...   hero(episode: $episode) {
        ...     name
        ...     friends @include(if: $withFriends) {
        ...       name
        ...     }
        ...   }
        ... }
        ... '''

        we have the directive

        >>> var_with_friends = Variable(name="withFriends", type="Boolean!")
        >>> directive_if = Directive(
        ...     name="include",
        ...     arguments=[
        ...         Argument(name="if", value=var_with_friends)
        ...     ]
        ... )

    """

    name: str
    arguments: List[Argument] = PydanticField(default_factory=list)

    _template_directive: Template = template_env.get_template("directive.jinja2")

    def render(self) -> str:
        return self._template_directive.render(
            name=self.name, arguments=[self._line_shift(argument.render()) for argument in self.arguments]
        )


class Field(_GraphQL2PythonQuery):
    """GraphQL Field type.

    See https://graphql.org/learn/queries/#fields for more details.

    Attributes:
        name: The field name.
        alias: The field alias.
        arguments: All arguments for the field.
        fields: All sub-fields for the field.
        directives: All field directives.
        typename: Add meta field `__typename` to sub-fields.

    Example:

        In the query

        .. code-block:: python

        >>> query_string = '''
        ... {
        ...   query {
        ...     field1 {
        ...       __typename
        ...       field2 {
        ...         __typename
        ...         f1
        ...         f2
        ...         f3
        ...       }
        ...     }
        ...   }
        ... }
        ... '''

        we have the following fields

        >>> Field(
        ...     name="field1",
        ...     fields=[
        ...         Field(
        ...             name="field2",
        ...             fields=["f1", Field(name="f2"), "f3"],
        ...             typename=True
        ...         )
        ...     ],
        ...     typename=True
        ... )

    """

    name: str
    alias: Optional[str] = PydanticField(default=None)
    arguments: List[Argument] = PydanticField(default_factory=list)
    fields: List[Union[str, 'Field', 'InlineFragment', 'Fragment']] = PydanticField(default_factory=list)
    directives: List[Directive] = PydanticField(default_factory=list)
    typename: bool = PydanticField(default=False, description="Add meta field `__typename` to sub-fields.")

    _template: Template = template_env.get_template("field.jinja2")

    def render(self) -> str:
        return self._template.render(
            name=self.name,
            alias=self.alias,
            arguments=[self._line_shift(argument.render()) for argument in self.arguments],
            fields=[self._render_field(field) for field in self.fields],
            directives=[directive.render() for directive in self.directives],
            typename=self.typename,
        )


class InlineFragment(_GraphQL2PythonQuery):
    """Inline Fragment GraphQL type.

    See https://graphql.org/learn/queries/#inline-fragments for more details.

    Attributes:
        type: A GraphQL type for the inline fragment.
        arguments: All arguments for the inline fragment.
        fields: All sub-fields for the inline fragment.
        typename: Add meta field `__typename` to sub-fields.

    Example:

        In the query

        >>> query_string = '''
        ... query HeroForEpisode($ep: Episode!) {
        ...   hero(episode: $ep) {
        ...     name
        ...     ... on Droid {
        ...       primaryFunction
        ...     }
        ...     ... on Human {
        ...       height
        ...     }
        ...   }
        ... }
        ... '''

        we have two inline fragments

        >>> inline_fragment_droid = InlineFragment(type="Droid", fields=["primaryFunction"])
        >>> inline_fragment_human = InlineFragment(type="Human", fields=["height"])

    """

    type: str
    arguments: List[Argument] = PydanticField(default_factory=list)
    fields: List[Union[str, 'Field', 'InlineFragment', 'Fragment']] = PydanticField(default_factory=list)
    typename: bool = PydanticField(default=False, description="Add meta field `__typename` to sub-fields.")

    _template: Template = template_env.get_template("inline_fragment.jinja2")

    def render(self) -> str:
        return self._template.render(
            type=self.type,
            arguments=[self._line_shift(argument.render()) for argument in self.arguments],
            fields=[self._render_field(field) for field in self.fields],
            typename=self.typename,
        )


class Fragment(_GraphQL2PythonQuery):
    """GraphQL fragment type.

    See https://graphql.org/learn/queries/#fragments for more details.

    Attributes:
        name: The fragment name.
        type: A GraphQL type for the fragment.
        fields: All sub-fields for the fragment.
        typename: Add meta field `__typename` to sub-fields.

    Example:

        In the query

        >>> query_string = '''
        ... {
        ...   leftComparison: hero(episode: EMPIRE) {
        ...     ...comparisonFields
        ...   }
        ...   rightComparison: hero(episode: JEDI) {
        ...     ...comparisonFields
        ...   }
        ... }
        ...
        ... fragment comparisonFields on Character {
        ...   name
        ...   appearsIn
        ...   friends {
        ...     name
        ...   }
        ... }
        ... '''

        we have the fragment

        >>> fragment_comparisonFields = Fragment(
        ...     name="comparisonFields",
        ...     type="Character",
        ...     fields=["name", "appearsIn", Field(name="friends", fields=["name"])]
        ... )

    """

    name: str
    type: str
    fields: List[Union[str, 'Field', 'InlineFragment', 'Fragment']] = PydanticField(default_factory=list)
    typename: bool = PydanticField(default=False, description="Add meta field `__typename` to sub-fields")

    _template: Template = template_env.get_template("fragment.jinja2")

    def render(self) -> str:
        return self._template.render(
            name=self.name,
            type=self.type,
            fields=[self._render_field(field) for field in self.fields],
            typename=self.typename,
        )


class Query(_GraphQL2PythonQuery):
    """GraphQL query type.

    See https://graphql.org/learn/queries/ for more details.

    Attributes:
        name: The query name.
        alias: An optional query alias.
        arguments: All query arguments.
        typename: Add meta field `__typename` to the query.
        fields: All sub-fields for the query.

    Example:

        For the query

        >>> query_string = '''
        ... {
        ...   human: human1000th(id: "1000") {
        ...     name
        ...     height
        ...   }
        ... }
        ... '''

        we have

        >>> human = Query(
        ...     name="human",
        ...     alias="human1000th",
        ...     arguments=[
        ...         Argument(name="id", value='"1000"')
        ...     ],
        ...     fields=["name", "height"]
        ... )

    """

    name: str
    alias: Optional[str] = PydanticField(default=None)
    arguments: List[Argument] = PydanticField(default_factory=list)
    typename: bool = PydanticField(default=False, description="Add meta field `__typename` to the query.")
    fields: List[Union[str, 'Field', 'InlineFragment', 'Fragment']] = PydanticField(default_factory=list)

    _template: Template = template_env.get_template("query.jinja2")

    def render(self) -> str:
        return self._template.render(
            name=self.name,
            alias=self.alias,
            arguments=[self._line_shift(argument.render()) for argument in self.arguments],
            typename=self.typename,
            fields=[self._render_field(field) for field in self.fields],
        )


class Operation(_GraphQL2PythonQuery):
    """GraphQL operation type.

    See https://graphql.org/learn/queries/ for more details.

    Attributes:
        type: A operation type.
        name: An optional operation name.
        variables: All operation variables.
        queries: All operation queries.
        fragments: All fragments for the operation.

    Example:

        For the query

        >>> query_string = '''
        ... mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!) {
        ...   createReview(episode: $ep, review: $review) {
        ...     stars
        ...     commentary
        ...   }
        ... }
        ... '''

        we have

        >>> var_ep = Variable(name="ep", type="Episode!")
        >>> var_review = Variable(name="review", type="ReviewInput!")
        >>>
        >>> Operation(
        ...     type="mutation",
        ...     name="CreateReviewForEpisode",
        ...     variables=[var_ep, var_review],
        ...     queries=[
        ...         Query(
        ...             name="createReview",
        ...             arguments=[
        ...                 Argument(name="episode", value=var_ep),
        ...                 Argument(name="review", value=var_review),
        ...             ],
        ...             fields=["stars", "commentary"]
        ...         ),
        ...     ],
        ... )

    """

    type: str = PydanticField(default="query", description="https://graphql.org/learn/queries")
    name: Optional[str] = PydanticField(default=None, description="https://graphql.org/learn/queries/#operation-name")
    variables: List[Variable] = PydanticField(
        default_factory=list, description="https://graphql.org/learn/queries/#fragments"
    )
    queries: List[Query] = PydanticField(default_factory=list, description="Queries for this GraphQL operation.")
    fragments: List[Fragment] = PydanticField(
        default_factory=list, description="https://graphql.org/learn/queries/#fragments"
    )

    _template: Template = template_env.get_template("operation.jinja2")
    _supported_types = ["query", "mutation", "subscription"]

    def render(self) -> str:
        return self._template.render(
            type=self.type,
            name=self.name,
            variables=[self._line_shift(variable.render()) for variable in self.variables],
            queries=[self._line_shift(query.render()) for query in self.queries],
            fragments=[fragment.render() for fragment in self.fragments],
        )


Variable.update_forward_refs()
Argument.update_forward_refs()
Field.update_forward_refs()
InlineFragment.update_forward_refs()
Fragment.update_forward_refs()
Query.update_forward_refs()
Operation.update_forward_refs()
