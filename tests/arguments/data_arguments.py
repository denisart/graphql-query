from graphql_query import Query, Argument, Operation

user_id = '"69fa0d2e-f7e8-410c-be50-24a03804cb4c"'
confirmation_id = '"63f65921-66cf-400a-aa05-71446b3621d2"'
password = '"87654321"'
password_confirm = '"87654321"'


query_no_fields_kwarg = Query(
    name='resetPassword',
    arguments=[
        Argument(
            name='userId',
            value=user_id,
        ),
        Argument(
            name='confirmationId',
            value=confirmation_id,
        ),
        Argument(
            name='password',
            value=password,
        ),
        Argument(
            name='passwordConfirm',
            value=password_confirm,
        ),
    ],
)

operation_no_fields_kwarg = Operation(
    type='mutation',
    name='ResetPassword',
    queries=[query_no_fields_kwarg],
)

expected_result_no_fields_kwarg = """mutation ResetPassword {
  resetPassword(
    userId: "69fa0d2e-f7e8-410c-be50-24a03804cb4c"
    confirmationId: "63f65921-66cf-400a-aa05-71446b3621d2"
    password: "87654321"
    passwordConfirm: "87654321"
  )
}"""
