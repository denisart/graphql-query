import pytest

from graphql_query import Argument

from .data_arguments import operation_no_fields_kwarg, expected_result_no_fields_kwarg


@pytest.mark.parametrize(
    'operation, result',
    [
        (operation_no_fields_kwarg, expected_result_no_fields_kwarg),
    ],
)
def test_valid_query_with_no_fields_kwarg(operation: Argument, result: str):
    assert operation.render() == result
