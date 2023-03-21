# Contributing to graphql_query

## Step 1.

Clone your fork and cd into the repo directory

```bash
git clone git@github.com:<your username>/graphql_query.git
cd graphql_query
```

## Step 2.

Set up a virtualenv for running tests

```bash
python3 -m venv venv/
source venv/bin/activate
```

## Step 3.

Install graphql_query, dependencies, test dependencies and doc dependencies

```bash
make install
```

## Step 4.

Checkout a new branch and make your changes

```bash
git checkout -b my-new-feature-branch
# make your changes...
```

## Step 5.

Fix formatting and imports

```bash
make format
# graphql_query uses black to enforce formatting and isort to fix imports
# (https://github.com/ambv/black, https://github.com/timothycrosley/isort)
```

## Step 6.

Run tests and linting

```bash
make
# there are a few sub-commands in Makefile like `test`, `testcov` and `lint`
# which you might want to use, but generally just `make` should be all you need
```

## Step 7.

... commit, push, and create your pull request
