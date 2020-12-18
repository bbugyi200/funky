.PHONY: help
help:  ## Print this message.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

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

.PHONY: check
check: check-python check-shell ## Run all tests.

.PHONY: check-python
check-python: ## Run Python tests.
	@printf "\n%s\n" "---------- Running Python Tests ----------"
	$(PWD)/tests/runtests $(pytest_opts)

.PHONY: check-shell
check-shell: ## Run Shell tests.
	@printf "\n%s\n" "---------- Running Shell Tests ----------"
	PYTHONPATH=$(PWD):$(PYTHONPATH) $(PWD)/tests/scripts/shell/test_funky.sh

.PHONY: release
release: dist ## Package and upload a release.
	twine upload dist/*

dist: clean ## Builds source and wheel package.
	python setup.py sdist
	ls -l dist

.PHONY: install
install: clean ## Install the package to the active Python's site-packages.
	python setup.py install
