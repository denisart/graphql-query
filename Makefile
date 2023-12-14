.DEFAULT_GOAL := all
sources = graphql_query/ tests/

.PHONY: install
install:
	python -m pip install -U pip
	python -m pip install -r requirements/requirements.txt
	python -m pip install -e ."[dev, test, docs]"

.PHONY: requirements-build
requirements-build:
	@echo "Updating requirements/*.txt files using pip-compile"
	find requirements/ -name '*.txt' ! -name 'all.txt' -type f -delete
	pip-compile --resolver=backtracking --output-file=requirements/requirements.txt pyproject.toml
	pip-compile --extra=dev --resolver=backtracking --output-file=requirements/requirements-dev.txt pyproject.toml
	pip-compile --extra=test --resolver=backtracking --output-file=requirements/requirements-test.txt pyproject.toml
	pip-compile --extra=docs --resolver=backtracking --output-file=requirements/requirements-docs.txt pyproject.toml

.PHONY: format
format:
	black $(sources)
	ruff --fix $(sources)

.PHONY: lint
lint:
	ruff $(sources)
	black $(sources) --check --diff

.PHONY: typecheck
typecheck:
	mypy graphql_query

.PHONY: testcov
testcov: test
	@echo "building coverage html"
	@coverage html

.PHONY: test
test:
	coverage run -m pytest --durations=10

.PHONY: all
all: lint typecheck testcov

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -rf site
	rm -rf docs/_build
	rm -rf docs/.changelog.md docs/.version.md docs/.tmp_schema_mappings.html
	rm -rf coverage.xml
