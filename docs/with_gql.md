# With gql

It is the simple example for usage of **graphql-query** with [gql 3](https://gql.readthedocs.io/en/stable/index.html).
How to install **gql 3** you can see [here](https://gql.readthedocs.io/en/stable/intro.html#installation).

## Basic Usage

For the Basic usage of **gql 3** with **graphql-query** you can to run the following code

```python
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql_query import Operation, Query

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://countries.trevorblades.com/")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# generating of GraphQL query string with graphql_query
getContinents = Operation(
    type="query",
    name="getContinents",
    queries=[Query(name="continents", fields=["code", "name"])]
)

# Provide a GraphQL query
query = gql(getContinents.render())

# Execute the query on the transport
result = client.execute(query)
print(result)
# {'continents': [{'code': 'AF', 'name': 'Africa'}, {'code': 'AN', 'name': 'Antarctica'}, {'code': 'AS', 'name': 'Asia'}, {'code': 'EU', 'name': 'Europe'}, {'code': 'NA', 'name': 'North America'}, {'code': 'OC', 'name': 'Oceania'}, {'code': 'SA', 'name': 'South America'}]}
```

## Using variables

GraphQL variables it is easy

```python
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql_query import Argument, Operation, Query, Variable

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://countries.trevorblades.com/")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# generating of GraphQL query string with graphql_query
code = Variable(name="code", type="ID!")

getContinentName = Operation(
    type="query",
    name="getContinentName",
    variables=[code],
    queries=[
        Query(
            name="continent",
            arguments=[Argument(name="code", value=code)],
            fields=["name"]
        )
    ]
)

query = gql(getContinentName.render())

params = {"code": "EU"}

# Get name of continent with code "EU"
result = client.execute(query, variable_values=params)
print(result)
# {'continent': {'name': 'Europe'}}

params = {"code": "AF"}

# Get name of continent with code "AF"
result = client.execute(query, variable_values=params)
print(result)
# {'continent': {'name': 'Africa'}}
```
