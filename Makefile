.PHONY: help
help:  ## Print this message.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.PHONY: all
all: test lint ## Run all tests and lint checks.

.PHONY: clean
clean: clean-build clean-pyc clean-test ## Remove all build, test, coverage and Python artifacts.

.PHONY: clean-build
clean-build: ## Remove build artifacts.
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## Remove test and coverage artifacts.
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

.PHONY: test
test: test-python test-shell ## Run all tests.

.PHONY: test
test-python: check-python ## Run Python tests.

.PHONY: test
test-shell: check-shell ## Run Shell tests.

.PHONY: check
check: check-python check-shell

.PHONY: check-python
check-python:
	@printf "\n%s\n" "---------- Running Python Tests ----------"
	tox -e py -- -v --cov --cov-fail-under=90 --cov-branch

.PHONY: check-shell
check-shell:
	@printf "\n%s\n" "---------- Running Shell Tests ----------"
	$(PWD)/tests/scripts/shell/test_funky.sh

.PHONY: release
release: dist ## Package and upload a release.
	twine upload dist/*

dist: clean ## Builds source and wheel package.
	python setup.py sdist
	ls -l dist

.PHONY: install
install: clean ## Install the package to the active Python's site-packages.
	python setup.py install

.PHONY: lint
lint: black isort flake8 mypy pylint ## Run all linting checks.

.PHONY: black
black: ## Run black checks. 
	python -m black --check funky
	python -m black --check tests

.PHONY: isort
isort: ## Run isort checks. 
	python -m isort --check-only funky
	python -m isort --check-only tests

.PHONY: mypy
mypy: ## Run mypy checks. 
	python -m mypy funky
	python -m mypy tests

.PHONY: flake8
flake8: ## Run flake8 checks. 
	python -m flake8 funky
	python -m flake8 tests

.PHONY: pylint
pylint: ## Run pylint checks. 
	pylint funky
	pylint tests
