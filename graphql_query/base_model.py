from typing import List, Optional, Type, Union, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo as PydanticFieldInfo

from .types import Argument, Directive, Field, InlineFragment


def _get_field_template(field_info: PydanticFieldInfo) -> Field:
    alias: Optional[str] = None
    arguments: List[Argument] = []
    directives: List[Directive] = []
    typename: bool = False

    if field_info.json_schema_extra is not None:
        alias = field_info.json_schema_extra.get("graphql_alias", None)
        arguments = field_info.json_schema_extra.get("graphql_arguments", [])
        directives = field_info.json_schema_extra.get("graphql_directives", [])
        typename = field_info.json_schema_extra.get("graphql_typename", False)

    return Field(name="<NAME>", fields=[], alias=alias, arguments=arguments, directives=directives, typename=typename)


def _get_fields(model: Type['GraphQLQueryBaseModel']) -> List[Field]:
    fields = []

    for f_name, f in model.model_fields.items():
        _field_template = _get_field_template(f)
        _field_template.name = f_name

        #
        # list type
        #
        if (hasattr(f.annotation, "__origin__")) and (f.annotation.__origin__ is list):
            list_args = get_args(f.annotation)[0]

            _field_template.name = f_name
            _field_template.fields = _get_fields(list_args)

        #
        # union type
        #
        elif get_origin(f.annotation) is Union:
            union_args = [union_arg for union_arg in get_args(f.annotation) if union_arg is not type(None)]

            if len(union_args) == 1:
                _field_template.name = f_name
                _field_template.fields = _get_fields(union_args[0])

            else:
                _field_template.name = f_name
                _field_template.fields = [
                    InlineFragment(type=union_arg.__name__, fields=_get_fields(union_arg)) for union_arg in union_args
                ]

        #
        # custom type
        #
        elif issubclass(f.annotation, GraphQLQueryBaseModel):
            _field_template.fields = _get_fields(f.annotation)

        fields.append(_field_template)

    return fields


class GraphQLQueryBaseModel(BaseModel):
    """A base class for GraphQL query data-model."""

    @classmethod
    def graphql_fields(cls) -> List[Field]:
        return _get_fields(cls)
