# =======================================================================
#
# Copyright (c) 2020-2023 Northern Capital Gateway, LLC. All rights reserved.
#
# This software is the confidential and proprietary information of
# Northern Capital Gateway, LLC.
# You shall not disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into with
# Northern Capital Gateway, LLC
#
# =======================================================================

import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

__all__ = [
    "_template_key_value",
    "_template_key_values",
    "_template_key_argument",
    "_template_key_variable",
    "_template_key_arguments",
    "_template_key_objects",
    "_template_directive",
    "_template_variable",
    "_template_operation",
    "_template_query",
    "_template_fragment",
    "_template_inline_fragment",
    "_template_field",
]


# templates setting for render of classes
TEMPLATES_FOLDER = Path(os.path.join(os.path.dirname(__file__), "templates/"))

template_env = Environment(loader=FileSystemLoader(searchpath=TEMPLATES_FOLDER))


_template_key_value: Template = template_env.get_template("argument_key_value.jinja2")
_template_key_values: Template = template_env.get_template("argument_key_values.jinja2")
_template_key_argument: Template = template_env.get_template("argument_key_argument.jinja2")
_template_key_variable: Template = template_env.get_template("argument_key_variable.jinja2")
_template_key_arguments: Template = template_env.get_template("argument_key_arguments.jinja2")
_template_key_objects: Template = template_env.get_template("argument_key_objects.jinja2")
_template_directive: Template = template_env.get_template("directive.jinja2")
_template_variable: Template = template_env.get_template("variable.jinja2")
_template_operation: Template = template_env.get_template("operation.jinja2")
_template_query: Template = template_env.get_template("query.jinja2")
_template_fragment: Template = template_env.get_template("fragment.jinja2")
_template_inline_fragment: Template = template_env.get_template("inline_fragment.jinja2")
_template_field: Template = template_env.get_template("field.jinja2")
