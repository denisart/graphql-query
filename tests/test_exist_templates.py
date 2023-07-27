import pytest
from jinja2 import Template

from graphql_query.templates import template_env


@pytest.mark.parametrize(
    "template_name",
    [
        # for Variable
        "variable.jinja2",
        # for Argument
        "argument_key_value.jinja2",
        "argument_key_values.jinja2",
        "argument_key_argument.jinja2",
        "argument_key_variable.jinja2",
        "argument_key_arguments.jinja2",
        "argument_key_objects.jinja2",
        # for Directive
        "directive.jinja2",
        # for Field
        "field.jinja2",
        # for InlineFragment
        "inline_fragment.jinja2",
        # for Fragment
        "fragment.jinja2",
        # for Query
        "query.jinja2",
        # for Operation
        "operation.jinja2",
    ],
)
def test_exist_templates_for_query(template_name: str):
    tpl = template_env.get_template(template_name)
    assert isinstance(tpl, Template)
